from subprocess import run
import os

print("Installing modules")
run(["pipenv", "install", "--quiet", "-r", "requirements.txt"])
print("Done")

import mysql.connector as sql

running = 5
while running:
    rootUser = input("Enter User with root privilages: ")
    rootPass = input("Enter Password: ")
    host = input("Enter Host: ")
    if host.strip() == "":
        host = "localhost"

    try:
        db = sql.connect(user=rootUser, passwd=rootPass, host=host)
        running = 0
    except:
        running -= 1
        print(
            f"Incorrect Input! Please check and try again. Attempts Remaining {running}"
        )
        if running == 0:
            exit("Error! Too Many Attempts")

mycursor = db.cursor()

if (input("DROP BANK IF EXIST? y/N: ").lower().strip() == "y"):
    mycursor.execute("DROP DATABASE IF EXISTS BANK;")

mycursor.execute(f"CREATE DATABASE IF NOT EXISTS BANK;")
db.connect(database="BANK")

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS BANK
(
BRANCH_ID VARCHAR(3) PRIMARY KEY,
NAME VARCHAR(20),
LOCATION VARCHAR(10),
ADMINISTRATOR INT
);""")

mycursor.execute(
"""
CREATE TABLE IF NOT EXISTS PERSON
(
PERSON_ID INT PRIMARY KEY AUTO_INCREMENT,
NAME VARCHAR(30),
GENDER CHAR(1),
ADDRESS VARCHAR(50),
DOB DATE
);
""")

mycursor.execute(
"""CREATE TABLE IF NOT EXISTS ACCOUNT
(
ACCOUNT_NO INT PRIMARY KEY AUTO_INCREMENT,
BALANCE INT,
ACCOUNT_TYPE CHAR(1),
MOBILE INT,
BRANCH_ID VARCHAR(3),
ADMINISTRATOR CHAR(1),
PERSON_ID INT,
FOREIGN KEY (PERSON_ID) REFERENCES PERSON(PERSON_ID) ON DELETE CASCADE,
FOREIGN KEY (BRANCH_ID) REFERENCES BANK(BRANCH_ID) ON DELETE CASCADE
);"""
)

mycursor.execute(
"""CREATE TABLE IF NOT EXISTS LOGIN_INFO
(
USERNAME VARCHAR(20),
PASSWORD VARCHAR(20),
ACCOUNT_NO INT,
PRIMARY KEY(ACCOUNT_NO,USERNAME),
FOREIGN KEY(ACCOUNT_NO) REFERENCES ACCOUNT(ACCOUNT_NO) ON DELETE CASCADE
);"""
)
mycursor.execute(
"""
CREATE TABLE IF NOT EXISTS LOAN(
LOAN_ID INT PRIMARY KEY AUTO_INCREMENT,
TOTAL_AMOUNT INT,
INTREST INT,
AMOUNT_LEFT INT,
OFFERED_BY VARCHAR(3),
OFFERED_TO INT,
FOREIGN KEY(OFFERED_BY) REFERENCES BANK(BRANCH_ID) ON DELETE CASCADE,
FOREIGN KEY(OFFERED_TO) REFERENCES ACCOUNT(ACCOUNT_NO) ON DELETE CASCADE
);""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS TRANSACTIONS
(
TRANSACTION_ID INT PRIMARY KEY AUTO_INCREMENT,
AMOUNT INT,
TRANSACTION_DATE DATE,
REMARKS VARCHAR(50),
TO_ACC INT,
FROM_ACC INT,
FOREIGN KEY (TO_ACC) REFERENCES ACCOUNT(ACCOUNT_NO) ON DELETE SET NULL,
FOREIGN KEY(FROM_ACC) REFERENCES ACCOUNT(ACCOUNT_NO) ON DELETE SET NULL
);"""
)

for file in ["BANK", "PERSON", "ACCOUNT", "LOGIN_INFO", "LOAN", "TRANSACTIONS"]:
    print("Inserting >>>>>", file)
    mycursor.execute(f'''
LOAD DATA LOCAL INFILE "{os.path.join(".","mockData",file+".csv")}"
INTO TABLE {file}
FIELDS TERMINATED BY ","
IGNORE 1 ROWS;
''')

db.commit()
with open("DB_DATA.txt", "w") as dbData:
    dbData.write(f"{host},{rootUser},{rootPass},BANK")

mycursor.execute("SET @@global.sql_mode= '';")

print(
    """
AcNo (9) : admin
Passwd : admin
"""
)


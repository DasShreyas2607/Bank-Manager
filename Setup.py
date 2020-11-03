from subprocess import run

print("Installing modules")
run(["pip", "install", "--quiet", "-r", "requirements.txt"])
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
mycursor.execute(f"CREATE DATABASE IF NOT EXISTS BANK;")
db.connect(database="BANK")

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS profile(AcNo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
 Name VARCHAR(50),
 DOB DATE,
 Nationality VARCHAR(5),
 Password VARCHAR(250),
 City VARCHAR(50),
 Address VARCHAR(250),
 username VARCHAR(10),
 AcType VARCHAR(20),
 Caste VARCHAR(20),
 MobileNo VARCHAR(20),
 Gender VARCHAR(10),
 Admin TINYINT(1) DEFAULT 0,
 Balance NUMERIC DEFAULT 0);"""
)
print("profile table created!!")

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS transactions(prID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                 FromAc VARCHAR(10),
                 ToAc VARCHAR(10),
                 Amount NUMERIC,
                 DOT DATE,
                 Remarks VARCHAR(250));"""
)
print("transactions table created!!")


mycursor.execute(
    f"INSERT IGNORE INTO profile(Name,DOB,Nationality,Password,City,Address,username,AcType,Caste,MobileNo,Gender,Admin) VALUES('Admin','2000-01-01','IN','pass','Banglore','NIL','ADMIN','Staff','NIL','+091 123 456 7809','Male',1);"
)

db.commit()
with open("DB_DATA.txt", "w") as dbData:
    dbData.write(f"{host},{rootUser},{rootPass},BANK")

mycursor.execute("SET @@global.sql_mode= '';")
print(
    """
AcNo (admin) : admin
Passwd : pass
"""
)

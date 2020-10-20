import mysql.connector as sql
import pandas as pd
import numpy as np

data1 = pd.read_csv("ProfileData.csv")
data2 = pd.read_csv("TransactionsData.csv")



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
mycursor.execute(f"CREATE OR REPLACE DATABASE BANKMGMT;")
db.connect(database="BANKMGMT")

mycursor.execute("SHOW TABLES;")
chkLst1 = ["profile", "transactions"]
tablelist = list(i[0] for i in mycursor)
failLst = []

for i in chkLst1:
    if i in tablelist:
        tablelist.remove(i)
        print(i, "-Passed!!")
    else:
        failLst.append(i)
        print(i, "-Failed!!")

if failLst:
    print("Creating desired tables")
if "profile" in failLst:
    mycursor.execute(
        """CREATE TABLE profile(ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
     UName VARCHAR(50),
     DOB DATE,
     Nationality VARCHAR(5),
     Password VARCHAR(250),
     City VARCHAR(50),
     Address VARCHAR(250),
     AcNo VARCHAR(10),
     AcType VARCHAR(20),
     Caste VARCHAR(20),
     MobileNo VARCHAR(20),
     Gender VARCHAR(10),
     Admin TINYINT(1) DEFAULT 0,
     Balance NUMERIC DEFAULT 0);"""
    )
    print("profile table created!!")
if "transactions" in failLst:
    mycursor.execute(
        """CREATE TABLE transactions(prID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                     FromAc VARCHAR(10),
                     ToAc VARCHAR(10),
                     Amount NUMERIC,
                     DOT DATE,
                     Remarks VARCHAR(250));"""
    )
    print("transactions table created!!")
# XYAECS!G
ch = input('Insert 1000 Profile and 999 000 Transaction mock ? Y: ')
if ch.lower().strip() == 'y':
    print("Inserting values\nPlease wait")

    print("Inserting into <profile>")
    counter = 0
    for i in data1.values:
        try:
            print(f"Inserting:{tuple(i)}")
            mycursor.execute(f"INSERT INTO profile VALUES{tuple(i)}")
            counter += 1
            if not counter % 5000:
                db.commit()
        except:
            print('Skipped Already Existing')


    print("Inserting into <transactions>")
    counter = 0
    for j in data2.values:
        try:
            print(f"Inserting:{tuple(j)}")
            mycursor.execute(f"INSERT INTO transactions VALUES{tuple(j)}")
            counter += 1
            if not counter % 5000:
                db.commit()

        except:
            print('Skipped Already Existing')
try:
    mycursor.execute(f"INSERT INTO profile(UName,DOB,Nationality,Password,City,Address,AcNo,AcType,Caste,MobileNo,Gender,Admin) VALUES('Admin','2000-01-01','IN','pass','Banglore','NIL','ADMIN','Staff','NIL','+091 123 456 7809','Male',1);")
except:
    print('Admin Already Inserted')

print('''
AcNo (admin) : ADMIN
Passwd : pass
''')
db.commit()

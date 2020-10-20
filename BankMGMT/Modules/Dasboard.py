from tkinter import Tk
from tkinter.ttk import *
import mysql.connector
import threading
from datetime import *
import random
import numpy as np
from PIL import Image, ImageTk
from time import sleep
import Modules.graph as graph

#
#
#
#
file = open(r"DB_DATA.txt", "r")
dbData = file.readline().split(",")
mydb = mysql.connector.connect(
    host=dbData[0],
    user=dbData[1],
    passwd=dbData[2],
    database=dbData[3],
)
file.close()
#
#
#
#
mycursor = mydb.cursor(buffered=True)


class dasboard(Frame):
    def __init__(self, root, acno):
        super().__init__(root)
        self.AcNo = acno
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.setupUI()

    def setupUI(self):
        mycursor.execute(f"SELECT Balance FROM profile where AcNo = '{self.AcNo}';")

        self.container = Frame(self, relief="ridge")
        self.container.grid(row=0, column=1, ipadx=10, ipady=2)

        mycursor.execute(
            f"SELECT Uname,DOB,Nationality,City,Address,AcNo,AcType,Caste,MobileNo,Gender FROM profile WHERE AcNo = '{self.AcNo}';"
        )
        self.dasblabels = dict(
            zip(
                (
                    "Name",
                    "DOB",
                    "Nationality",
                    "City",
                    "Address",
                    "A/c No",
                    "A/c Type",
                    "Caste",
                    "Mobile No",
                    "Gender",
                ),
                mycursor.fetchone(),
            )
        )
        mydb.close()
        self.sep = Separator(self.container, orient="vertical").grid(
            row=0, rowspan=999, column=2, sticky="ns", padx=10
        )
        self.iter = 0
        self.clno = 0
        for txt in self.dasblabels.keys():
            self.container.grid_rowconfigure(self.iter, minsize=40)
            self.tempLabel = Label(self.container, text=txt).grid(
                column=self.clno, row=self.iter, sticky="w", padx=8, pady=5
            )
            self.tempLabel = Label(self.container, text=self.dasblabels[txt]).grid(
                column=self.clno + 1, row=self.iter, sticky="e", padx=8, pady=5
            )
            if self.iter == 4:
                self.iter = 0
                self.clno += 3
            else:
                self.iter += 1
        self.sync()

    def sync(self):
        with open(r"DB_DATA.txt", "r") as file:
            dbData = file.readline().split(",")
        mydb = mysql.connector.connect(
            host=dbData[0],
            user=dbData[1],
            passwd=dbData[2],
            database=dbData[3],
        )
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(
            f"SELECT SUM(Amount),DOT from transactions WHERE ToAc = '{self.AcNo}' GROUP BY DOT ORDER BY DOT DESC LIMIT 10;"
        )
        self.toData = mycursor.fetchall()
        self.toDataDic = {}
        for i in self.toData:
            self.toDataDic[i[1]] = i[0]
        mycursor.execute(
            f"SELECT SUM(Amount),DOT from transactions WHERE FromAc = '{self.AcNo}' GROUP BY DOT ORDER BY DOT DESC LIMIT 10;"
        )
        self.fromData = mycursor.fetchall()
        self.fromDataDic = {}
        for i in self.fromData:
            self.fromDataDic[i[1]] = i[0]
        self.graph = graph.Graph(self, 5, 3)
        self.graph.grid(row=0, column=0, padx=10)
        self.graph.add_subplot("line")
        self.data = {}
        for key in sorted(self.fromDataDic.keys() | self.toDataDic.keys()):
            if key in self.fromDataDic.keys() and key in self.toDataDic.keys():
                self.data[key] = self.toDataDic[key] - self.fromDataDic[key]
            elif key in self.fromDataDic.keys():
                self.data[key] = -self.fromDataDic[key]
            else:
                self.data[key] = self.toDataDic[key]
        self.y = list(self.data.values())
        self.x = [i for i in range(len(self.y))]
        self.graph.plot("line", x=self.x, y=self.y)
        mydb.close()

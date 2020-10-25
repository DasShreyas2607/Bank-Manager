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

class dasboard(Frame):
    def __init__(self, root, acno):
        super().__init__(root)
        self.root = root
        self.acno = acno
        self.sync()
        threading.Thread(target=self.syncTimer).start()

    def setupUI(self, root, acno):
        self.AcNo = acno
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.cursor.execute(f"SELECT Balance FROM profile where AcNo = '{self.AcNo}';")

        self.container = Frame(self, relief="ridge")
        self.container.grid(row=0, column=1, ipadx=10, ipady=2)

        self.cursor.execute(
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
                self.cursor.fetchone(),
            )
        )
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

        self.cursor.execute(
            f"SELECT IF(ToAc = '{self.acno}',Amount,0),IF(FromAc='{self.acno}',Amount,0) FROM transactions ORDER BY prID DESC;"
        )
        self.Data = self.cursor.fetchall()
        self.graph = graph.Graph(self, 5, 3)
        self.graph.grid(row=0, column=0, padx=10)
        self.graph.add_subplot("line")
        self.graph.plot("line",self.Data)


    def sync(self):
        with open(r"DB_DATA.txt", "r") as file:
            dbData = file.readline().split(",")
        self.db = mysql.connector.connect(
            host=dbData[0],
            user=dbData[1],
            passwd=dbData[2],
            database=dbData[3],
        )
        self.cursor = self.db.cursor(buffered=True)
        self.setupUI(self.root, self.acno)

    def syncTimer(self):
        try:
            while True and self.winfo_exists():
                sleep(20)
                self.container.destroy()
                self.sync()
        except:
            pass

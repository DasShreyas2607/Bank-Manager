from tkinter import Tk
from tkinter.ttk import *
import mysql.connector
import threading
from time import sleep
import Modules.graph as graph


class dasboard(Frame):
    def __init__(self, root, username):
        super().__init__(root)
        self.root = root
        self.username = username
        self.container = None
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.sync()
        self.syncGraph()
        threading.Thread(target=self.syncTimer).start()

    def setupUI(self, root, username):
        self.username = username
        self.cursor.execute(
            f"SELECT ACCOUNT_NO FROM LOGIN_INFO WHERE USERNAME= '{self.username}';"
        )
        self.acno = self.cursor.fetchone()[0]
        self.cursor.execute(
            f"SELECT BALANCE FROM ACCOUNT where ACCOUNT_NO = '{self.acno}';"
        )
        if self.container:
            self.container.destroy()
        self.container = Frame(self, relief="ridge")
        self.container.grid(row=0, column=1, ipadx=10, ipady=2)

        self.cursor.execute(
            f"SELECT A.ACCOUNT_NO,P.NAME,P.DOB,P.ADDRESS,L.USERNAME,A.ACCOUNT_TYPE,A.MOBILE,P.GENDER FROM ACCOUNT A INNER JOIN PERSON P ON A.PERSON_ID = P.PERSON_ID INNER JOIN LOGIN_INFO L ON A.ACCOUNT_NO = L.ACCOUNT_NO WHERE L.USERNAME = '{self.username}';"
        )
        self.dasblabels = dict(
            zip(
                (
                    "A/c No",
                    "Name",
                    "DOB",
                    "ADDRESS",
                    "User Name",
                    "A/c Type",
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
            if self.iter == 5:
                self.iter = 0
                self.clno += 3
            else:
                self.iter += 1

    def syncGraph(self):
        try:
            self.graph.destroy()
        except:
            pass
        self.graph = graph.Graph(self, 5, 3)
        self.graph.grid(row=0, column=0, padx=10)
        self.graph.add_subplot("line")
        self.cursor.execute(
            f"SELECT IF(TO_ACC = '{self.dasblabels['A/c No']}',AMOUNT,0), IF(FROM_ACC='{self.dasblabels['A/c No']}',AMOUNT,0) FROM TRANSACTIONS ORDER BY TRANSACTION_ID DESC;"
        )
        self.Data = self.cursor.fetchall()
        self.graph.plot("line", self.Data)

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
        self.setupUI(self.root, self.username)

    def syncTimer(self):
        try:
            iter__ = 0
            while self.winfo_exists():
                sleep(1)
                iter__ += 1
                if iter__ == 10:
                    iter__ = 0
                    self.container.destroy()
                    self.sync()
                    sleep(2)
                    self.syncGraph()
        except:
            pass

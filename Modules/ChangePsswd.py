from tkinter import Tk, StringVar
from tkinter.ttk import *
import mysql.connector
import threading


class change(Frame):
    def __init__(self, root, username):
        super().__init__(root)
        self.sync()
        self.SetupUI(root, username)

    def SetupUI(self, root, username):
        self.container = Frame(self)
        self.container.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.username = username
        #
        self.pssdlb = Label(self.container, text=" ")
        self.pssdlb.grid(row=1, columnspan=2)
        self.labeldic = {}
        self.row = 2
        self.column = 0
        self.labels = ["New Password", "Confirm Password"]
        for label in self.labels:
            self.label = Label(self.container, text=label)
            self.label.grid(row=self.row, column=self.column, padx=3, pady=3)
            self.labeldic[label] = Entry(self.container, show="*")
            self.labeldic[label].grid(
                row=self.row, column=self.column + 1, padx=3, pady=3
            )
            self.row += 1
        self.changePsswdBtn = Button(
            self.container, text="Change", command=self.changepsd
        )
        self.changePsswdBtn.grid()

    def changepsd(self):
        if (
            self.labeldic["New Password"].get()
            and self.labeldic["New Password"].get()
            == self.labeldic["Confirm Password"].get()
            and 8 < len(self.labeldic["New Password"].get()) < 245
        ):
            self.dbcommit()
        else:
            self.pssdlb["text"] = "Password criteria not satisfied!"

    def dbcommit(self):
        self.sync()
        self.cursor.execute(
            f"UPDATE profile SET Password = '{self.labeldic['New Password'].get()}' WHERE username = '{self.username}' "
        )
        self.db.commit()
        self.pssdlb["text"] = "Password Updated ! Takes effect after restart"

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

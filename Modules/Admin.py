from tkinter import Tk, StringVar, IntVar, Toplevel
from tkinter.ttk import *
from tkcalendar import *
import mysql.connector
import threading
from time import sleep
from datetime import *


class admin(Frame):
    def __init__(self, root, username=None):
        super().__init__(root)
        self.username = username
        self.errBx = None
        self.message = StringVar()
        self.sync()
        self.container = Frame(self)
        self.container.grid(row=1, column=0)
        self.msg = Label(self, textvariable=self.message)
        self.msg.grid(row=0, column=0, sticky="s")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)
        #
        self.usernamelabel = Label(self.container, text="User Name")
        self.usernameen = Entry(self.container)
        self.usernameen.bind("<KeyRelease>", self.pressed)
        self.usernamelabel.grid(row=0, column=0, padx=3, pady=3)
        self.usernameen.grid(
            row=0, column=1, columnspan=3, sticky="wens", padx=3, pady=3
        )
        self.savebtnvar = StringVar()
        self.savebtnvar.set("Save")
        self.savebtn = Button(
            self.container, textvariable=self.savebtnvar, command=self.save
        )
        self.savebtn.grid(row=8, column=2, columnspan=2, sticky="wens", padx=3, pady=3)
        #
        self.delete = Button(self.container, text="Close", command=self.close)
        self.delete.grid(row=8, column=0, columnspan=2, sticky="wens", padx=3, pady=3)
        #
        self.labeldic = {}
        self.row = 1
        self.column = 0
        #
        self.validate = (self.register(self.validation), "%P", "%W")
        #
        # fmt: off
        self.labels = [
            'ACCOUNT NO','BALANCE','ACCOUNT TYPE',
            'MOBILE','BRANCH ID', 'PERSON ID',
            'NAME', 'ADDRESS', 'PASSWORD'
        ]
        # fmt: on
        self.AlwaysTrue = True
        for label in self.labels:
            self.label = Label(self.container, text=label)
            self.label.grid(row=self.row, column=self.column, padx=3, pady=3)
            self.textVar = StringVar()
            self.labeldic[label] = (
                Entry(
                    self.container,
                    validate="focusout",
                    validatecommand=self.validate,
                    textvariable=self.textVar,
                    name=label.lower(),
                ),
                self.textVar,
            )
            self.labeldic[label][0].grid(
                row=self.row, column=self.column + 1, padx=3, pady=3
            )
            if self.row == len(self.labels) // 2 and self.AlwaysTrue:
                self.column = 2
                self.row = 0
                self.AlwaysTrue = False
            self.row += 1
        #
        #
        self.genders = ["F", "M"]
        self.gender = StringVar()
        self.isAdmin = IntVar()
        #
        self.genlb = Label(self.container, text="GENDER")
        self.genlb.grid(row=self.row - 1, column=0, padx=3, pady=3)
        self.genContainer = Frame(self.container)
        for gen in self.genders:
            b = Radiobutton(
                self.genContainer, text=gen, value=gen, variable=self.gender
            )
            b.pack(side="left")
        self.genContainer.grid(row=self.row - 1, column=1, padx=3, pady=3)
        #
        self.adminlb = Label(self.container, text="ADMIN")
        self.adminlb.grid(row=self.row, column=2, padx=3, pady=3)
        self.adminen = Checkbutton(self.container, variable=self.isAdmin)
        self.adminen.grid(row=self.row, column=3, padx=3, pady=3)
        #
        self.doblb = Label(self.container, text="DOB")
        self.doblb.grid(row=self.row, column=0)
        self.today = datetime.now()
        try:
            self.maxdate = self.today.replace(year=self.today.year - 18)
        except ValueError:
            self.maxdate = self.today.replace(
                year=self.today.year - 18, day=self.today - 1
            )
        self.dob = DateEntry(
            self.container, maxdate=self.maxdate, date_pattern="dd/mm/yyyy"
        )
        self.dob.grid(row=self.row, column=1, sticky="we")
        if username != None:
            self.usernameen.insert(0, username)
            self.pressed()

    def pressed(self, key=None):
        threading.Thread(target=self.search(self.usernameen.get())).start()

    def search(self, username):
        self.sync()
        threading.Thread(
            self.cursor.execute(
                f"SELECT A.ACCOUNT_NO, A.BALANCE, A.ACCOUNT_TYPE, A.MOBILE, A.BRANCH_ID, P.PERSON_ID, P.NAME, P.ADDRESS, L.PASSWORD, P.DOB, P.GENDER, A.ADMINISTRATOR FROM ACCOUNT A INNER JOIN PERSON P ON A.PERSON_ID = P.PERSON_ID INNER JOIN LOGIN_INFO L ON A.ACCOUNT_NO = L.ACCOUNT_NO WHERE L.USERNAME = '{self.usernameen.get()}';"
            )
        ).start()
        self.data = self.cursor.fetchone()
        if self.data:
            index = 0
            for key in self.labeldic.keys():
                self.labeldic[key][-1].set(str(self.data[index]))
                self.update()
                index += 1
            self.isAdmin.set(int(1 if self.data[-1] == 'T' else 0))
            self.gender.set(self.data[-2])
            self.dob.set_date(self.data[-3])
            self.savebtnvar.set("Save")

        else:
            for key in self.labeldic.keys():
                self.labeldic[key][-1].set("")
                if self.usernameen.get():
                    self.savebtnvar.set("Add")

    def save(self):
        for entry, var_ in self.labeldic.values():
            if not entry.get():
                self.message.set("All fields are Mandatory")
                try:
                    threading.Thread(target=self.messageTimer).start()
                except RuntimeError:
                    pass
                return 0
        try:
            if not self.data:
                self.cursor.execute(
                    f"INSERT INTO LOGIN_INFO(USERNAME, ACCOUNT_NO) VALUES('{self.usernameen.get()}', {self.labeldic['ACCOUNT_NO'].get()});"
                )
                self.db.commit()
        except:
            pass

        # P.NAME, P.ADDRESS, L.PASSWORD, P.DOB, P.GENDER,
        self.cursor.execute(
                f"UPDATE ACCOUNT SET BALANCE='{self.labeldic['BALANCE'][1].get()}', ACCOUNT_TYPE='{self.labeldic['ACCOUNT TYPE'][1].get()}', MOBILE='{self.labeldic['MOBILE'][1].get()}', BRANCH_ID='{self.labeldic['BRANCH ID'][1].get()}', ADMINISTRATOR='{'T' if self.isAdmin.get() == 1 else 'F'}' WHERE ACCOUNT_NO = '{self.labeldic['ACCOUNT NO'][1].get()}';"
            )
        self.cursor.execute(
                f"UPDATE LOGIN_INFO SET PASSWORD='{self.labeldic['PASSWORD'][1].get()}' WHERE USERNAME='{self.usernameen.get()}';"
            )
        self.cursor.execute(
                f"UPDATE PERSON SET NAME='{self.labeldic['NAME'][1].get()}', ADDRESS='{self.labeldic['ADDRESS'][1].get()}', DOB='{self.dob.get_date()}', GENDER='{self.gender.get()}' WHERE PERSON_ID='{self.labeldic['PERSON ID'][1].get()}';"
            )

        # iter_ = 0
        # for values in self.labeldic.values():
        #     self.cursor.execute(
        #         f"UPDATE ACCOUNT SET {self.labels[iter_]}='{values[-1].get()}' WHERE username in ('{self.usernameen.get()}');"
        #     )
        #     iter_ += 1
        # self.cursor.execute(
        #     f"UPDATE profile SET Gender ='{self.gender.get()},DOB='{self.dob.get_date()}' WHERE username in ('{self.usernameen.get()}');"
        # )
        self.db.commit()
        self.db.close()
        self.sync()

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

    def close(self):
        try:
            if self.data and self.usernameen.get() != self.username:
                self.closeWin = Toplevel(self, bg="#454545")
                self.text = Label(
                    self.closeWin, text="Sure?? This can't be undone"
                ).pack()
                self.confirmBtn = Button(
                    self.closeWin, text="I understand, close Acc", command=self.closeAcc
                )
                self.confirmBtn.pack()
        except:
            pass

    def closeAcc(self):
        # self.cursor.execute(
        #     f"DELETE FROM profile WHERE username = '{self.usernameen.get()}';"
        # )
        self.cursor.execute(
                f"DELETE FROM ACCOUNT WHERE ACCOUNT_NO = {self.labeldic['ACCOUNT NO'].get()};"
            )
        self.cursor.execute(
                f"DELETE FROM WHERE USERNAME={self.usernameen.get()};"
            )
        self.cursor.execute(
                f"DELETE FROM WHERE PERSON_ID={self.labeldic['PERSON ID'].get()};"
            )
        self.db.commit()
        self.pressed()
        self.closeWin.destroy()

    def validation(self, word, label=None):
        text = label.split(".")[-1]
        if text == "password":
            if len(word) < 8:
                self.labeldic["PASSWORD"][0].focus_set()
                self.message.set("Password length should be atleast 8")
                try:
                    threading.Thread(target=self.messageTimer).start()
                except RuntimeError:
                    pass
                return False
            else:
                return True

    def messageTimer(self):
        try:
            sleep(5)
            self.message.set("")
        except:
            pass


class user(admin):
    def __init__(self, root, username):
        super().__init__(root, username)
        self.usernameen["state"] = "disabled"
        self.labeldic["PASSWORD"][0]["state"] = "disabled"
        self.labeldic["BALANCE"][0]["state"] = "disabled"
        self.labeldic["ACCOUNT TYPE"][0]["state"] = "disabled"
        self.labeldic["PASSWORD"][0]["show"] = "*"
        self.adminen.grid_forget()
        self.adminlb.grid_forget()
        self.delete.destroy()

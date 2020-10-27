from tkinter import Tk, StringVar, IntVar
from tkinter.ttk import *
from tkcalendar import *
import mysql.connector
import threading
from datetime import *


class admin(Frame):
    def __init__(self, root, acno=None):
        super().__init__(root)
        self.sync()
        threading.Thread(target=self.syncTimer).start()
        self.container = Frame(self)
        self.container.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #
        self.acnolabel = Label(self.container, text="A/c No")
        self.acnoen = Entry(self.container)
        self.acnoen.bind("<KeyRelease>", self.pressed)
        self.acnolabel.grid(row=0, column=0, padx=3, pady=3)
        self.acnoen.grid(row=0, column=1, columnspan=3, sticky="wens", padx=3, pady=3)
        self.savebtn = Button(self.container, text="Save", command=self.save)
        self.savebtn.grid(row=8, column=2, columnspan=2, sticky="wens", padx=3, pady=3)
        #
        self.labeldic = {}
        self.row = 1
        self.column = 0
        # fmt: off
        self.labels = [
            'Uname','Nationality',
            'Password','City','Address',
            'AcType','Caste','MobileNo',
            'Balance',
        ]
        # fmt: on
        for label in self.labels:
            self.label = Label(self.container, text=label)
            self.label.grid(row=self.row, column=self.column, padx=3, pady=3)
            self.labeldic[label] = Entry(self.container)
            self.labeldic[label].grid(
                row=self.row, column=self.column + 1, padx=3, pady=3
            )
            if self.row == len(self.labels) // 2:
                self.column = 2
                self.row = 0
            self.row += 1
        #
        #
        self.genders = ["Female", "Male"]
        self.gender = StringVar()
        self.isAdmin = IntVar()
        #
        self.genlb = Label(self.container, text="Gender")
        self.genlb.grid(row=8, column=0, padx=3, pady=3)
        self.genContainer = Frame(self.container)
        for gen in self.genders:
            b = Radiobutton(
                self.genContainer, text=gen, value=gen, variable=self.gender
            )
            b.pack(side="left")
        self.genContainer.grid(row=8, column=1, padx=3, pady=3)
        #
        #
        self.adminlb = Label(self.container, text="Admin")
        self.adminlb.grid(row=7, column=2, padx=3, pady=3)
        self.adminen = Checkbutton(self.container, variable=self.isAdmin)
        self.adminen.grid(row=7, column=3, padx=3, pady=3)
        #
        self.doblb = Label(self.container, text="DOB")
        self.doblb.grid(row=7, column=0)
        self.dob = DateEntry(self.container)
        self.dob.grid(row=7, column=1, sticky="we")
        #
        if acno != None:
            self.acnoen.insert(0, acno)
            self.pressed()

    def pressed(self, key=None):
        threading.Thread(target=self.search(self.acnoen.get())).start()

    def search(self, acno):
        self.sync()
        threading.Thread(
            self.cursor.execute(
                f"SELECT Uname,Nationality,Password,City,Address,AcType,Caste,MobileNo,Balance,DOB,Gender,Admin FROM profile WHERE AcNo = '{self.acnoen.get()}';"
            )
        ).start()
        self.data = self.cursor.fetchone()
        if self.data:
            index = 0
            for key in self.labeldic.keys():
                self.labeldic[key].delete(0, "end")
                self.labeldic[key].insert(0, str(self.data[index]))
                self.update()
                index += 1
            self.isAdmin.set(int(self.data[-1]))
            self.gender.set(self.data[-2])
            self.dob.set_date(self.data[-3])

        else:
            for key in self.labeldic.keys():
                self.labeldic[key].delete(0, "end")
                self.update()

    def save(self):
        try:
            if not self.data:
                self.cursor.execute(
                    f"INSERT INTO profile(AcNo) VALUES('{self.acnoen.get()}');"
                )
                self.db.commit()
        except:
            pass

        iter_ = 0
        for values in self.labeldic.values():
            self.cursor.execute(
                f"UPDATE profile SET {self.labels[iter_]}='{values.get()}' WHERE Acno in ('{self.acnoen.get()}');"
            )
            iter_ += 1
        self.cursor.execute(
            f"UPDATE profile SET Gender ='{self.gender.get()}',Admin ='{self.isAdmin.get()}',DOB='{self.dob.get_date()}' WHERE Acno in ('{self.acnoen.get()}');"
        )
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

    def syncTimer(self):
        try:
            while True and self.winfo_exists():
                sleep(20)
                self.container.destroy()
                self.sync()
                self.pressed()
        except:
            pass


class user(admin):
    def __init__(self, root, acno):
        super().__init__(root, acno)
        self.acnoen["state"] = "disabled"
        self.labeldic["Password"]["state"] = "disabled"
        self.labeldic["Balance"]["state"] = "disabled"
        self.labeldic["AcType"]["state"] = "disabled"
        self.labeldic["Password"]["show"] = "*"
        self.adminen.grid_forget()
        self.adminlb.grid_forget()

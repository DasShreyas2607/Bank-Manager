from tkinter import Tk, StringVar
from tkinter.ttk import *
from datetime import datetime
from time import sleep
import mysql.connector
import threading


class pay(Frame):
    def __init__(self, root, acno, bal):
        super().__init__(
            root,
        )
        self.acno = acno
        self.bal = bal
        self.sync()
        # threading.Thread(target=self.syncTimer).start()
        self.SetupUI(root, acno, bal)

    def SetupUI(self, root, acno, bal):
        self.container = Frame(self)
        self.container.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.acno = acno
        """self.cursor.execute(f"SELECT BALANCE FROM ACCOUNT WHERE ACCOUNT_ID = '{self.acno}';")
        self.Balance = self.cursor.fetchone()[0]"""
        #
        #
        #
        self.amntValidationCmd = (self.register(self.AmountValidate), "%P")
        self.getNameCmd = (self.register(self.getName), "%P")
        #
        self.Tolabel = Label(self.container, text="To")
        self.ToEntry = Entry(
            self.container, validate="all", validatecommand=self.getNameCmd
        )
        self.Namelabel = Label(self.container, text="Name")
        self.NameEntry = Entry(self.container, state="readonly")
        self.RemLabel = Label(self.container, text="Remarks")
        self.RemEntry = Entry(self.container)
        self.AmntLab = Label(self.container, text="Amount")
        self.AmntEntry = Entry(
            self.container, validate="all", validatecommand=self.amntValidationCmd
        )
        #
        self.PayBttn = Button(self.container, text="Pay", command=self.pay)
        #
        self.Tolabel.grid(row=0, column=0)
        self.ToEntry.grid(row=0, column=1)
        self.RemLabel.grid(row=2, column=0)
        self.RemEntry.grid(row=2, column=1)
        self.AmntLab.grid(row=3, column=0)
        self.AmntEntry.grid(row=3, column=1)
        self.NameEntry.grid(row=1, column=1)
        self.Namelabel.grid(row=1, column=0)
        self.PayBttn.grid(row=4, column=1, sticky="we")
        #
        self.confirmFrame = Frame(self)
        self.message = StringVar()
        self.message.set(" ")
        self.OMessage = Label(self.confirmFrame, textvariable=self.message)
        self.OMessage.pack()
        self.confirmFrame.place(relx=0.5, rely=0.25, anchor="center")
        #

    #
    def AmountValidate(self, amnt):
        try:
            amnt = int(amnt)
            if amnt > int(self.Balance):
                return False
            return True
        except:
            if amnt == "":
                return True
            return False

    def getName(self, name):
        if name:
            self.NameEntry.config(state="normal")
            self.NameEntry.delete(0, "end")
            self.cursor.execute(f"SELECT P.NAME FROM ACCOUNT A INNER JOIN PERSON P ON A.PERSON_ID = P.PERSON_ID WHERE A.ACCOUNT_NO = '{name}';")
            toName = self.cursor.fetchone()
            if toName:
                self.NameEntry.insert("end", str(toName[0]))
            (self.cursor.fetchone())
            self.NameEntry.config(state="readonly")
            self.update()
            return True
        else:
            self.NameEntry.config(state="normal")
            self.NameEntry.delete(0, "end")
            self.NameEntry.config(state="readonly")
            return True

    def pay(self):
        self.grid_propagate(flag=False)
        self.sync()
        threading.Thread(target=self.payNow).start()

    def payNow(self):
        self.data = []
        self.PayBttn.config(state="disabled")
        for entry in [self.ToEntry, self.RemEntry, self.AmntEntry]:
            self.data.append(entry.get())
            entry.config(state="disabled")
        if self.payIsValidate(self.data):
            self.Balance = str(int(self.Balance) - int(self.AmntEntry.get()))
            self.cursor.execute(
                f"INSERT INTO TRANSACTIONS(FROM_ACC,TO_ACC,AMOUNT,TRANSACTION_DATE,REMARKS) VALUES('{self.acno}','{self.data[0]}',{self.data[2]},'{datetime.now()}','{self.data[1]}');"
            )

            self.cursor.execute(
                f"UPDATE ACCOUNT SET BALANCE = '{self.Balance}' WHERE ACCOUNT_NO = '{self.acno}';"
            )

            self.cursor.execute(
                f"UPDATE ACCOUNT SET BALANCE = BALANCE + '{self.AmntEntry.get()}' WHERE ACCOUNT_NO = '{self.data[0]}';"
            )

            self.db.commit()
            self.db.close()
            self.sync()

            self.messageBox()
            for entry in [self.ToEntry, self.RemEntry, self.AmntEntry]:
                entry.delete(0, "end")
        for entry in [self.ToEntry, self.RemEntry, self.AmntEntry, self.PayBttn]:
            entry.config(state="normal")

    def payIsValidate(self, lst):
        if not self.AmntEntry.get():
            self.message.set(f"Enter Amount")
        elif not self.NameEntry.get():
            self.message.set(f"Invalid Payee")
        elif int(self.AmntEntry.get()) > int(self.Balance):
            self.message.set(f"Cannot pay more than Balance {self.Balance} ")
        elif int(self.AmntEntry.get()) >= int(self.Balance) - 500:
            self.message.set(f"Should be 500 less than Balance {self.Balance} ")
        elif int(self.AmntEntry.get()) < 100:
            self.message.set("Should be atleast 100")
        else:
            self.message.set(
                f"Payed to : {self.NameEntry.get()}\nAmount   : {self.AmntEntry.get()}\nRemarks  : {self.RemEntry.get()}"
            )
            return 1
        self.messageBox()
        return 0

    def messageBox(self):
        self.update()
        sleep(3)
        self.message.set(" ")

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
        self.cursor.execute(f"SELECT BALANCE FROM ACCOUNT WHERE ACCOUNT_NO = '{self.acno}';")
        self.Balance = self.cursor.fetchmany(1)[0][0]
        self.bal.set(self.Balance)

    def syncTimer(self):
        try:
            iter__ = 0
            while self.winfo_exists():
                sleep(1)
                iter__ += 1
                if iter__ == 10:
                    iter__ = 0
                    self.sync()
        except:
            pass


if __name__ == "__main__":
    win = Tk()
    app = pay(win, "test")
    app.grid()
    win.mainloop()

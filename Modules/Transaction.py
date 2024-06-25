from tkinter import Tk
from tkinter.ttk import *
from time import sleep
import mysql.connector
import threading


class transaction(Frame):
    def __init__(self, root, acno, bal):
        super().__init__(root)
        self.bal = bal
        self.container = Frame(self)
        self.container.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.offset = 0
        self.acno = acno
        #
        self.table = Treeview(self.container)
        self.table["columns"] = ("Account", "Amount", "Date", "Remarks")
        self.table.column("#0", width=0, minwidth=0)
        for i in self.table["columns"]:
            self.table.heading(i, text=i)
        self.nextbtn = Button(self.container, text="Next", command=self.next)
        self.refresh = Button(self.container, text="Sync", command=self.sync)
        self.prevbtn = Button(
            self.container, text="prev", command=self.prev, state="disabled"
        )
        #
        self.row, self.column = 0, 0
        self.table.grid(row=self.row, column=self.column, columnspan=2)
        self.row += 1
        self.prevbtn.grid(row=self.row, column=self.column, sticky="w")
        self.column += 1
        self.refresh.grid(row=self.row, column=self.column, sticky="e", padx=100)
        self.nextbtn.grid(row=self.row, column=self.column, sticky="e")
        self.sqlQuery = f"SELECT TO_ACC, AMOUNT, TRANSACTION_DATE, REMARKS FROM TRANSACTIONS WHERE FROM_ACC = '{self.acno}' OR TO_ACC = '{self.acno}' ORDER BY TRANSACTION_ID DESC LIMIT 10"
        self.sync()
        threading.Thread(target=self.syncTimer).start()

    def next(self):
        self.offset += 10
        if self.offset != 0:
            self.prevbtn.config(state="normal")
        self.sync()

    def prev(self):
        self.offset -= 10
        if self.offset == 0:
            self.prevbtn.config(state="disabled")
        self.sync()

    def sync(self):
        for item in self.table.get_children():
            self.table.delete(item)
        with open(r"DB_DATA.txt", "r") as file:
            dbData = file.readline().split(",")
        mydb = mysql.connector.connect(
            host=dbData[0],
            user=dbData[1],
            passwd=dbData[2],
            database=dbData[3],
        )
        mycursor = mydb.cursor(buffered=True)
        temp = self.sqlQuery + f" OFFSET {self.offset};"

        mycursor.execute(temp)
        self.transactionData = mycursor.fetchall()
        mydb.close()
        for tup in self.transactionData:
            self.table.insert("", "end", values=tup)

    def syncBal(self):
        if self.bal:
            with open(r"DB_DATA.txt", "r") as file:
                dbData = file.readline().split(",")
            mydb1 = mysql.connector.connect(
                host=dbData[0],
                user=dbData[1],
                passwd=dbData[2],
                database=dbData[3],
            )
            mycursor1 = mydb1.cursor(buffered=True)
            mycursor1.execute(
                f"SELECT BALANCE FROM ACCOUNT WHERE ACCOUNT_NO = '{self.acno}';"
            )
            self.balance = mycursor1.fetchone()
            mydb1.close()
            self.bal.set(self.balance[0])

    def syncTimer(self):
        try:
            iter__ = 0
            while self.winfo_exists():
                sleep(1)
                iter__ += 1
                if iter__ == 60:
                    iter__ = 0
                    self.sync()
                    self.syncBal()
        except:
            pass


class view(transaction):
    def __init__(self, root, acno):
        super().__init__(root, acno=acno, bal=None)
        self.table["columns"] = ("Account No", "UserName", "DOB", "Gender", "Admin")
        for i in self.table["columns"]:
            self.table.heading(i, text=i)
        self.sqlQuery = f"SELECT A.ACCOUNT_NO, L.USERNAME, P.DOB, P.Gender, IF(A.ADMINISTRATOR='T','Yes','No') FROM ACCOUNT A INNER JOIN PERSON P ON A.PERSON_ID = P.PERSON_ID INNER JOIN LOGIN_INFO L ON A.ACCOUNT_NO = L.ACCOUNT_NO WHERE BRANCH_ID=(SELECT BRANCH_ID FROM ACCOUNT WHERE ACCOUNT_NO = {acno}) ORDER BY ACCOUNT_NO DESC LIMIT 10"
        # SELECT TO_ACC, AMOUNT, TRANSACTION_DATE, REMARKS FROM TRANSACTIONS WHERE FROM_ACC = '{self.acno}' OR TO_ACC = '{self.acno}' ORDER BY TRANSACTION_ID DESC LIMIT 10;
        self.sync()

class loan(transaction):
    def __init__(self, root, acno, admin):
        super().__init__(root, acno=acno, bal=None)
        self.table["columns"] = ("TOTAL AMOUNT", "INTREST", "AMOUNT LEFT", "OFFERED BY", "OFFERED TO")
        for i in self.table["columns"]:
            self.table.heading(i, text=i)
        if admin == 'F':
            self.sqlQuery = f"SELECT TOTAL_AMOUNT, INTREST, AMOUNT_LEFT, OFFERED_BY, OFFERED_TO FROM LOAN WHERE OFFERED_TO={acno} ORDER BY LOAN_ID DESC LIMIT 10"
        else:
            self.sqlQuery = f"SELECT TOTAL_AMOUNT, INTREST, AMOUNT_LEFT, OFFERED_BY, OFFERED_TO FROM LOAN WHERE OFFERED_BY=(SELECT BRANCH_ID FROM ACCOUNT WHERE ACCOUNT_NO = {acno}) ORDER BY LOAN_ID DESC LIMIT 10"
        # SELECT TO_ACC, AMOUNT, TRANSACTION_DATE, REMARKS FROM TRANSACTIONS WHERE FROM_ACC = '{self.acno}' OR TO_ACC = '{self.acno}' ORDER BY TRANSACTION_ID DESC LIMIT 10;
        self.sync()
from tkinter import Tk
from tkinter.ttk import *
from time import sleep
import mysql.connector
import threading

class transaction(Frame):
    def __init__(self,root,acno,bal):
        super().__init__(root)
        self.bal=bal
        self.container = Frame(self)
        self.container.grid(row=0,column=0)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.offset = 0
        self.acno = acno
#
        self.table = Treeview(self.container)
        self.table['columns']=('To Account','Amount','Date','Remarks')
        self.table.column('#0',width=0,minwidth=0)
        for i in self.table['columns']:
            self.table.heading(i,text=i)
        self.nextbtn = Button(self.container,text='Next',command=self.next)
        self.prevbtn = Button(self.container,text='prev',command=self.prev,state='disabled')
        self.table.grid(row=0,column=0)
        self.nextbtn.grid(row=1,column=0,sticky='e')
        self.prevbtn.grid(row=1,column=0,sticky='w')
        self.sync()
        threading.Thread(target=self.syncTimer).start()

    def next(self):
        self.offset += 10
        if self.offset != 0:
            self.prevbtn.config(state='normal')
        self.sync()

    def prev(self):
        self.offset -= 10
        if self.offset == 0:
            self.prevbtn.config(state='disabled')
        self.sync()

    def sync(self):
        for item in self.table.get_children():
            self.table.delete(item)
        with open(r'DB_DATA.txt','r') as file:
            dbData = file.readline().split(',')
        mydb = mysql.connector.connect(
            host=dbData[0],
            user=dbData[1],
            passwd=dbData[2],
            database=dbData[3],
        )
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(
            f"SELECT ToAc, Amount, DOT, Remarks FROM transactions WHERE FromAc = '{self.acno}' OR ToAc = '{self.acno}' ORDER BY prID DESC LIMIT 10 OFFSET {self.offset};"
        )
        self.transactionData = mycursor.fetchall()
        mydb.close()
        for tup in self.transactionData:
            self.table.insert('','end',values=tup)
    def sync2(self):
        with open(r'DB_DATA.txt','r') as file:
            dbData = file.readline().split(',')
        mydb1 = mysql.connector.connect(
            host=dbData[0],
            user=dbData[1],
            passwd=dbData[2],
            database=dbData[3],
        )
        mycursor1 = mydb1.cursor(buffered=True)
        mycursor1.execute(
            f"SELECT Balance FROM profile WHERE AcNo = '{self.acno}';"
        )
        self.balance = mycursor1.fetchone()
        mydb1.close()
        self.bal.set(self.balance[0])
    def syncTimer(self):
        try:
            while True and self.winfo_exists():
                sleep(10)
                self.sync()
                self.sync2()
        except:
            pass

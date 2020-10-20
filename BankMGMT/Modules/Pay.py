from tkinter import Tk, StringVar
from tkinter.ttk import *
from datetime import datetime
from time import sleep
import mysql.connector
import threading





class pay(Frame):
    def __init__(self,root,AcNo,bal):
        super().__init__(root, )
        self.bal=bal
        self.container = Frame(self)
        self.container.grid(row=0,column=0)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.AcNo = AcNo
        mycursor.execute(f"SELECT Balance FROM profile WHERE AcNo = '{self.AcNo}';")
        self.Balance = mycursor.fetchone()[0]
        #
        #
#
        self.amntValidationCmd = (self.register(self.AmountValidate),'%P')
        self.getNameCmd = (self.register(self.getName),'%P')
#
        self.Tolabel = Label(self.container,text='To')
        self.ToEntry = Entry(self.container,validate='all',validatecommand=self.getNameCmd)
        self.Namelabel = Label(self.container,text='Name')
        self.NameEntry = Entry(self.container,state='readonly')
        self.RemLabel = Label(self.container,text='Remarks')
        self.RemEntry = Entry(self.container)
        self.AmntLab = Label(self.container, text="Amount")
        self.AmntEntry = Entry(self.container,validate='all',validatecommand=self.amntValidationCmd)
#
        self.PayBttn = Button(self.container,text='Pay',command=self.pay)
#
        self.Tolabel.grid(row=0,column=0)
        self.ToEntry.grid(row=0,column=1)
        self.RemLabel.grid(row=2,column=0)
        self.RemEntry.grid(row=2,column=1)
        self.AmntLab.grid(row=3,column=0)
        self.AmntEntry.grid(row=3,column=1)
        self.NameEntry.grid(row=1,column=1)
        self.Namelabel.grid(row=1,column=0)
        self.PayBttn.grid(row=4,column=1,sticky='we')
        #
        self.confirmFrame = Frame(self)
        self.message = StringVar()
        self.message.set(' ')
        self.OMessage = Label(self.confirmFrame,textvariable=self.message)
        self.OMessage.pack()
        self.confirmFrame.place(relx=0.5,rely=0.25,anchor='center')
        #
#
    def AmountValidate(self,amnt):
        try:
            amnt=int(amnt)
            if amnt > int(self.Balance):
                return False
            return True
        except:
            if amnt == '':
                return True
            return False

    def getName(self,name):
        if name:
            self.NameEntry.config(state='normal')
            self.NameEntry.delete(0,'end')
            mycursor.execute(f"SELECT Uname FROM profile WHERE AcNo = '{name}';")
            toName = mycursor.fetchone()
            if toName:
                self.NameEntry.insert('end',str(toName[0]))
            (mycursor.fetchone())
            self.NameEntry.config(state='readonly')
            self.update()
        return True
    def pay(self):
        self.grid_propagate(flag=False)
        threading.Thread(target=self.payNow).start()

    def payNow(self):
        self.data = []
        self.PayBttn.config(state='disabled')
        for entry in [self.ToEntry,self.RemEntry,self.AmntEntry]:
            self.data.append(entry.get())
            entry.config(state='disabled')
        if self.payIsValidate(self.data):
            self.Balance = str(int(self.Balance) - int(self.AmntEntry.get()))
            threading.Thread(target=mycursor.execute(f"INSERT INTO transactions(FromAc,ToAc,Amount,DOT,Remarks) VALUES('{self.AcNo}','{self.data[0]}',{self.data[2]},'{datetime.now()}','{self.data[1]}');"))
            threading.Thread(target=mycursor.execute(f"UPDATE profile SET Balance = '{self.Balance}' WHERE AcNo = '{self.AcNo}';"))
            threading.Thread(target=mycursor.execute(f"UPDATE profile SET Balance = Balance + '{self.AmntEntry.get()}' WHERE AcNo = '{self.data[0]}';"))
            mydb.commit()
            self.sync()
            self.messageBox()
            for entry in [self.ToEntry,self.RemEntry,self.AmntEntry]:
                entry.delete(0,'end')
        for entry in [self.ToEntry,self.RemEntry,self.AmntEntry,self.PayBttn]:
            entry.config(state='normal')
        

    def payIsValidate(self,lst):
        if not self.AmntEntry.get():
            self.message.set(f"Enter Amount")
        elif not self.NameEntry.get():
            self.message.set(f'Acc no Found')
        elif int(self.AmntEntry.get()) > int(self.Balance):
            self.message.set(f"Cannot pay more than Balance({self.Balance})")
        elif int(self.AmntEntry.get()) >= int(self.Balance) - 500:
            self.message.set(f"Should be 500 less than Balance({self.Balance})")
        elif int(self.AmntEntry.get()) < 100:
            self.message.set("Should be atleast 100")
        else:
            self.message.set(f'Payed to : {self.NameEntry.get()}\nAmount   : {self.AmntEntry.get()}\nRemarks  : {self.RemEntry.get()}')
            return 1
        self.messageBox()
        return 0

    def messageBox(self):
        self.update()
        sleep(3)
        self.message.set(' ')
        
    def sync(self):
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
            f"SELECT Balance FROM profile WHERE AcNo = '{self.AcNo}';"
        )
        self.balance = mycursor1.fetchone()
        mydb1.close()
        self.bal.set(self.balance[0])


#
#
#
#
file = open(r'DB_DATA.txt','r')
dbData = file.readline().split(',')
mydb = mysql.connector.connect(
    host=dbData[0],
    user=dbData[1],
    passwd=dbData[2],
    database=dbData[3],
)
file.close()
mycursor = mydb.cursor(buffered=True)
#
#
#
#
if __name__=='__main__':
    win=Tk()
    app = pay(win,'test')
    app.grid()
    win.mainloop()

from tkinter import Tk,StringVar,IntVar
from tkinter.ttk import *
from ttkthemes import ThemedStyle
from tkcalendar import *
import mysql.connector
import threading
from datetime import *
import random
from PIL import Image, ImageTk




class login(Frame):
    def __init__(self,root,func,bal):
        super().__init__(root)
        self.func = func
        self.bal = bal
        self.container = Frame(self)
        self.container.grid(row=0,column=0)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.AcNo = None
        self.logo = Image.open(r"./assets/logo.jpg")
        self.logotk = ImageTk.PhotoImage(self.logo)
        #
        self.labeldic = {}
        self.labels = ["A/c No", "Password"]
        self.row, self.column = (1,0)
        for label in self.labels:
            self.label = Label(self.container,text=label)
            self.label.grid(row=self.row,column=self.column,padx=3,pady=3)
            self.labeldic[label] = Entry(self.container)
            if label in ["Password"]:
                         self.labeldic[label].config(show='*')
            self.labeldic[label].grid(row=self.row,column=self.column+1,padx=3,pady=3)
            self.row += 1
        #
        self.button = Button(self.container,text='Login',command=self.login)
        self.button.grid(row=self.row,column=self.column+1,sticky='we',padx=3,pady=3)

    def login(self):
        mycursor.execute(
            f"SELECT UName FROM profile WHERE AcNo = '{self.labeldic['A/c No'].get()}' AND BINARY Password = '{self.labeldic['Password'].get()}';"
        )
        cursor = mycursor.fetchone()
        if cursor:
            self.AcNo = self.labeldic['A/c No'].get()
            self.container.destroy()
            self.update()
            self.progressbar()
            self.update()
        else:
            self.invl = Label(self.container, text="Invalid Entry, Try Again")
            self.invl.grid(row=0,column=0,columnspan=2)

    def progressbar(self):
        self.progress = Progressbar(
            self,
            orient='horizontal',
            length=200,
            mode="determinate",
        )
        self.prolabel = Label(self, text="Loading...")
        self.loginnamelabel = Label(self, text="SVK BANK", font=("Arial Black", 18))
        self.photo = Label(self, image=self.logotk)
        self.loginnamelabel.grid(row=0,column=1)
        self.photo.grid(row=0,column=0,rowspan=3,sticky='nwes')
        self.prolabel.grid(row=1,column=1)
        self.progress.grid(row=2,column=1)
        for i in range(0, 100, 4):
            self.progress["value"] = i
            self.update_idletasks()
            self.progress.after(random.randint(15, 100))
        else:
            self.progress.destroy()
            self.prolabel.destroy()
            self.photo.destroy()
            self.loginnamelabel.destroy()
            self.update()
            self.func()
            threading.Thread(target=mycursor.execute(f"SELECT Balance FROM profile WHERE AcNo = '{self.AcNo}';")).start()
            self.bal.set(f'{mycursor.fetchone()[0]}')
            self.destroy()

        


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

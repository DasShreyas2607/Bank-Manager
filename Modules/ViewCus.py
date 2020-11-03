from tkinter.ttk import *
from time import sleep
import mysql.connector
import threading
from tkinter import Tk


class view(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.container = Frame(self)
        self.container.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.offset = 0
        #
        self.table = Treeview(self.container)
        self.table["columns"] = ("Account No", "Name", "DOB", "Gender", "Admin")
        self.table.column("#0", width=0, minwidth=0)
        for i in self.table["columns"]:
            self.table.heading(i, text=i)
        self.nextbtn = Button(self.container, text="Next", command=self.next)
        self.refresh = Button(self.container, text="Sync", command=self.sync)
        self.prevbtn = Button(
            self.container, text="prev", command=self.prev, state="disabled"
        )
        self.table.grid(row=0, column=0, columnspan=2)
        self.refresh.grid(row=1, column=1, sticky="e", padx=100)
        self.nextbtn.grid(row=1, column=1, sticky="e")
        self.prevbtn.grid(row=1, column=0, sticky="w")
        self.sqlQuery = f"SELECT username,name,DOB,Gender,IF(Admin=1,'Yes','No') FROM profile ORDER BY ID DESC LIMIT 10 OFFSET {self.offset};"
        self.bind("<ButtonRelease>", self.selectItem)
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

    def selectItem(self):
        curItem = self.table.focus()
        print(self.table.item(curItem))

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
        mycursor.execute(self.sqlQuery)
        self.CustData = mycursor.fetchall()
        mydb.close()
        for tup in self.CustData:
            self.table.insert("", "end", values=tup)

    def syncTimer(self):
        try:
            while True and self.winfo_exists():
                sleep(60)
                self.sync()
        except:
            pass


if __name__ == "__main__":
    win = Tk()
    app = view(win)
    app.grid()
    win.mainloop()

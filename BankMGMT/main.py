from tkinter import Tk, StringVar
from tkinter.ttk import Notebook, Label, Frame, Style
import mysql.connector
from ttkthemes import ThemedStyle
import threading
import sys
from PIL import Image, ImageTk
from Modules import Admin, Dashboard, ChangePsswd, Login, Pay, Transaction

#
#
#
#
file = open(r"DB_DATA.txt", "r")
dbData = file.readline().split(",")
mydb = mysql.connector.connect(
    host=dbData[0],
    user=dbData[1],
    passwd=dbData[2],
    database=dbData[3],
)
file.close()
mycursor = mydb.cursor(buffered=True)
mycursor.execute("SET @@global.sql_mode= '';")
mydb.commit()
#
#
#
#


class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

    def setupUI(self, master, theme):
        self.master = master
        self.theme = theme
        self.username = None
        self.TkBal = StringVar()
        self.Admin = None
        #
        self.MainFrame = Frame(self)
        self.headerFrame = Frame(self.MainFrame)
        self.headerFrame.grid_columnconfigure(1, weight=1)
        self.head = Label(
            self.headerFrame, text="SVK BANKING SYSTEMS", font=("Arial", 18)
        )
        self.ballb = Label(self.headerFrame, text="Balance:    ", font=("Arial", 18))
        self.ballb2 = Label(
            self.headerFrame, textvariable=self.TkBal, font=("Arial", 18)
        )
        self.head.grid(row=0, column=0, sticky="w")
        self.headerFrame.pack(fill="x")
        self.MainFrame.pack(fill="both", expand=True)
        self.update
        #
        self.login()

    def login(self):
        self.loginContainer = Login.login(self.MainFrame, self.panel, self.TkBal)
        self.loginContainer.place(relx=0.5, rely=0.5, anchor="center")

    def panel(self):
        self.ballb.grid(row=0, column=1, sticky="e")
        self.ballb2.grid(row=0, column=2, sticky="e")
        self.username = self.loginContainer.username
        mycursor.execute(
            f"SELECT AcNo FROM profile WHERE username = '{self.username}';"
        )
        self.acno = mycursor.fetchone()[0]
        style = Style(self)
        style.configure("leftTab.TNotebook", tabposition="s")
        style.theme_settings(
            self.theme, {"TNotebook.Tab": {"configure": {"padding": [10, 10]}}}
        )
        self.notebook = Notebook(
            self.MainFrame, style="leftTab.TNotebook", width=800, height=500
        )
        self.notebook.pack(expand=True, fill="both")
        self.notebook.bind("<<NotebookTabChanged>>", self.logout)
        self.tabs = {
            "Dashboard": Dashboard.dashboard(self.notebook, self.username),
            "Transactions": Transaction.transaction(
                self.notebook, self.acno, self.TkBal
            ),
            "Pay": Pay.pay(self.notebook, self.acno, self.TkBal),
            "Change Password": ChangePsswd.change(self.notebook, self.username),
            "Settings": Admin.user(self.notebook, self.username),
        }
        mycursor.execute(
            f"SELECT Admin FROM profile WHERE username = '{self.username}';"
        )
        self.images = {}
        self.Tkimages = {}
        self.ImageIter = 0
        for image in [
            "Dashboard",
            "Transactions",
            "Pay",
            "Change Password",
            "Settings",
            "add_user",
            "view",
            "leave",
        ]:
            self.images[image] = Image.open(f".//assets//{image}.png")
            self.images[image].thumbnail((30, 30), Image.ANTIALIAS)
            self.Tkimages[image] = ImageTk.PhotoImage(self.images[image])

        for tab in self.tabs.keys():
            self.notebook.add(
                self.tabs[tab],
                text=tab,
                image=self.Tkimages[tab.strip()],
                compound="top",
            )
            self.ImageIter += 1

        if mycursor.fetchone()[0]:
            self.notebook.add(
                Admin.admin(self.notebook, self.username),
                text="Add/Edit Ac",
                image=self.Tkimages["add_user"],
                compound="top",
            )
            self.notebook.add(
                Transaction.view(self.notebook),
                text="View Clients",
                image=self.Tkimages["view"],
                compound="top",
            )

        self.notebook.add(
            Frame(), text="Logout", image=self.Tkimages["leave"], compound="top"
        )

    def logout(self, key=None):
        try:
            if key.widget.select() == self.notebook.tabs()[-1]:
                self.master.quit()
                self.master.destroy()
                mydb.close()
                with open("isExit", "w") as isExit:
                    isExit.write("true")
                sys.exit()
        except:
            pass


if __name__ == "__main__":
    #
    win = Tk()
    #
    theme = "breeze"
    style = ThemedStyle(win)
    style.theme_use(theme)
    #
    win.geometry("1250x600")
    logo = Image.open(r"./assets/logo.jpg")
    logotk = ImageTk.PhotoImage(logo)
    win.iconphoto(True, logotk)
    win.title("SVK BANKING SYSTEMS")
    win.resizable(False, False)
    #
    app = App(win)
    app.setupUI(win, theme)
    app.pack(expand=True, fill="both")
    app.mainloop()

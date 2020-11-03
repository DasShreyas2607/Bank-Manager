from tkinter.ttk import *

self.notebook = Notebook(
    self.MainFrame, style="leftTab.TNotebook", width=800, height=500
)
self.notebook.pack(expand=True, fill="both")
self.notebook.bind("<<NotebookTabChanged>>", self.logout)
self.tabs = {
    "Dasboard": Dasboard.dasboard(self.notebook, self.AcNo),
    "Transactions": Transaction.transaction(self.notebook, self.AcNo, self.TkBal),
    "Pay": Pay.pay(self.notebook, self.AcNo, self.TkBal),
    "Change Password": ChangePsswd.change(self.notebook, self.AcNo),
    "Settings": Admin.user(self.notebook, self.AcNo),
}
mycursor.execute(f"SELECT Admin FROM profile WHERE AcNo = '{self.AcNo}';")
self.images = {}
self.Tkimages = {}
self.ImageIter = 0
for image in [
    "Dasboard",
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

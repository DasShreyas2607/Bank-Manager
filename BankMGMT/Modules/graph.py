from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Tk
from tkinter.ttk import Frame


class Graph(Frame):
    def __init__(self,master,sizey,sizex):
        super().__init__(master)
        self.figure = Figure(figsize=(sizey, sizex),facecolor='#474747')
        self.subPlots = {}
        canvas = FigureCanvasTkAgg(self.figure, master=self)
        canvas.get_tk_widget().pack(expand=1)

    def add_subplot(self,name,int_=111):
        self.subPlots[name] = self.figure.add_subplot(int_)

    def plot(self,name,x,y):
        self.subPlots[name].plot(x,y)
        self.subPlots[name].axis('off')

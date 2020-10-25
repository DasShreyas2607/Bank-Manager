from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Tk
from tkinter.ttk import Frame
from scipy.ndimage.filters import gaussian_filter1d as filt
import numpy as np


class Graph(Frame):
    def __init__(self, master, sizey, sizex):
        super().__init__(master)
        self.figure = Figure(figsize=(sizey, sizex), facecolor="#474747")
        self.subPlots = {}
        canvas = FigureCanvasTkAgg(self.figure, master=self)
        canvas.get_tk_widget().pack(expand=1)

    def add_subplot(self, name, int_=111):
        self.subPlots[name] = self.figure.add_subplot(int_)

    def plot(self, name, lst):
        grph = [int(FR-TO) for TO,FR in lst]
        ind = np.arange(len(lst))
        self.subPlots[name].plot(ind, filt(grph[::-1],sigma=0.75),':',color='Brown')
        self.subPlots[name].axis("off")

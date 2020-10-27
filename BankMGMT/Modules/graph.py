from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Tk
from tkinter.ttk import Frame
from scipy.ndimage.filters import gaussian_filter1d as filt
from scipy.interpolate import interp1d
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
        try:
            grph = [int(FR - TO) for TO, FR in lst]
            ind = np.arange(len(lst))
            f = interp1d(ind, grph[::-1], kind="cubic")
            nind = np.linspace(0, len(lst) - 1, 750)
            self.subPlots[name].clear()
            self.subPlots[name].plot(nind, f(nind), "--", color="red")
            self.subPlots[name].axis("off")
        except:
            pass

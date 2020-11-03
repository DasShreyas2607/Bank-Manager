from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Tk
from tkinter.ttk import Frame
from scipy.ndimage.filters import gaussian_filter1d as filt
from scipy.interpolate import interp1d
import numpy as np
from time import sleep
import threading


class Graph(Frame):
    def __init__(self, master, sizey, sizex):
        super().__init__(master)
        self.tg = 1
        self.figure = Figure(figsize=(sizey, sizex), facecolor="#454545")
        self.subPlots = {}
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(expand=1)

    def add_subplot(self, name, int_=111):
        self.subPlots[name] = self.figure.add_subplot(int_)

    def plot(self, name, lst):
        if True:
            if lst:
                grph = [int(FR) for TO, FR in lst if int(FR) != 0]
                grph2 = [int(TO) for TO, FR in lst if int(TO) != 0]
                if 3 >= len(grph) >= 2:
                    kind_ = "linear"
                elif len(grph) > 3:
                    kind_ = "cubic"

                if 3 >= len(grph2) >= 2:
                    kind2_ = "linear"
                elif len(grph2) > 3:
                    kind2_ = "cubic"

                if len(grph) >= 2:
                    ind = np.arange(len(grph))
                    f = interp1d(ind, grph[::-1], kind=kind_)
                    nind = np.linspace(0, len(grph) - 1, 750)
                    self.subPlots[name].plot(
                        ind, grph[::-1], "o", nind, f(nind), color="red"
                    )

                if len(grph2) >= 2:
                    ind2 = np.arange(len(grph2))
                    f2 = interp1d(ind2, grph2[::-1], kind=kind2_)
                    nind2 = np.linspace(0, len(grph2) - 1, 750)
                    self.subPlots[name].plot(
                        ind2, grph2[::-1], "o", nind2, f2(nind2), color="green"
                    )
            self.subPlots[name].axis("off")
            sleep(1)

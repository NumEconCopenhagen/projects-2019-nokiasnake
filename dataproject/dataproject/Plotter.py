import tkinter as tk
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class DataPlotter:
    
    def __init__(self,figure):
        
        self.fig = figure
        self.subplots = {}
    
    def addlineplot(self,data,plotname,**kwargs):
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]
        currentplot = self.fig.add_subplot(1,1,1)
        currentplot.plot(data[xaxisname],data[yaxisname], **kwargs)
        currentplot.set_xlabel(xaxisname)
        currentplot.set_ylabel(yaxisname)
        currentplot.grid(True)
        currentplot.legend()
        self.subplots[plotname]=currentplot
    
    def addtwinxlineplot(self, data, plotname,color="b"):
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]
        currentplot = self.subplots[plotname].twinx()
        currentplot.plot(data[xaxisname],data[yaxisname],color=color)
        currentplot.set_ylabel(yaxisname)
        self.subplots[plotname+"twinx"]=currentplot

    def addbarplot(self,data,plotname, color="g"):
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]
        currentplot = self.fig.add_subplot(1,1,1)
        currentplot.bar(data[xaxisname],data[yaxisname],color=color)
        currentplot.set_xlabel(xaxisname)
        currentplot.set_ylabel(yaxisname)
        self.subplots[plotname]=currentplot
    
    def addsplitbarplot(self,data,plotname):
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]
        
        positive = data[yaxisname].copy()
        negative = data[yaxisname].copy()
        positive[positive<=0] = np.nan
        negative[negative> 0] = np.nan

        currentplot = self.fig.add_subplot(1,1,1)
        currentplot.bar(data[xaxisname],positive,color="g")
        currentplot.bar(data[xaxisname],negative,color="r")
        currentplot.set_xlabel(xaxisname)
        currentplot.set_ylabel(yaxisname)
        currentplot.axhline(y=0,color="k")
        
        self.subplots[plotname]=currentplot

    def figuretitle(self, figuretitle):
        self.fig.suptitle(figuretitle)

    def clearplots(self):
        self.fig.clear()
        self.subplots.clear()



class PlotterWindow:
    def __init__(self, data, slicename, graphtype, xvariable=None, yvariablelist=None, xsize=1280, ysize=720):

        self.xsize = xsize
        self.ysize = ysize
        self.data = data

        self.xvariable = xvariable
        self.yvariablelist = yvariablelist
        
        self.graphtype = graphtype


        self.window = tk.Tk()

        self.currentslicekey = tk.StringVar()
        
        self.slicename = slicename
        self.slicekeys = (self.data[self.slicename].unique())

        self.graphmenuframe = tk.Frame(self.window)
        self.graphmenu = tk.OptionMenu(self.graphmenuframe, self.currentslicekey, *self.slicekeys, command = lambda x: self.ongraphmenuchange())
        self.graphnamelabel = tk.Label(self.graphmenuframe, text="Municipality: ")
        self.graphnamelabel.pack(side=tk.LEFT)
        self.graphmenu.pack(side=tk.LEFT)
        self.graphmenuframe.pack()

        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self.window)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)

        self.canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand = True)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH, expand = True)
        
        self.window.geometry(str(self.xsize) + "x" + str(self.ysize))

        self.plotter = DataPlotter(self.figure)

    def start(self):
        self.window.mainloop()
    
    def ongraphmenuchange(self):
        self.updateplotter(self.currentslicekey.get())
        self.canvas.draw()

    def updateplotter(self, graphnamekey):
        self.plotter.clearplots()

        self.plotter.figuretitle(graphnamekey)
        newplotdata = self.data.loc[self.data[self.slicename] == graphnamekey,:]
        
        if self.graphtype=="piplot":
            for index, yvariable in enumerate(self.yvariablelist):
                self.plotter.addlineplot(newplotdata[[self.xvariable,yvariable]],"plot"+str(index+1))
        
        if self.graphtype=="Standard":
            self.plotter.addsplitbarplot(newplotdata[[self.xvariable,self.yvariablelist[0]]],"plot1")
            self.plotter.addtwinxlineplot(newplotdata[[self.xvariable,self.yvariablelist[1]]],"plot1")
        
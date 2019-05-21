#importing necessary libraries. Check readme.md for installation tips
import tkinter as tk
import pandas as pd 
import numpy as np 
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_finance import candlestick_ochl

#Define the dataplotter class responsible for drawing the figures used in the graphwindow
class DataPlotter:
    #Defining the __init__ function
    def __init__(self,figure):
        
        self.fig = figure
        self.subplots = {}
    
    def addlineplot(self,data,plotname,**kwargs):
        """Creates a line subplot for the dataplotter figure based on the data. 1st column
        on horizontal axis, 2nd column on the vertical axis. 

        Args:
            data (Pandas DataFrame): 2-column dataframe. 
            plotname (String): Name for the subplot
            **kwargs
        """

        #Assign column name as variable
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]

        #Construct the subplot 
        currentplot = self.fig.add_subplot(1,1,1)
        currentplot.plot(data[xaxisname],data[yaxisname], **kwargs)
        currentplot.set_xlabel(xaxisname)
        currentplot.set_ylabel(yaxisname)
        currentplot.grid(True)
        currentplot.legend()
        
        #Add the subplot to the subplot dictionary in __init__
        self.subplots[plotname]=currentplot

    def addcandlestick(self,data,plotname):
        """Creates a candlestick subplot for the dataplotter figure based on the data
        """
        currentplot = self.fig.add_subplot(1,1,1)
        candlestick_ochl(currentplot,data,colorup="g")
        currentplot.set_xlabel("Iteration")
        currentplot.grid(True)
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
        self.graphnamelabel = tk.Label(self.graphmenuframe, text="Pi=")
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
        
        if self.graphtype=="candlestick":
            lower = 0
            upper = len(list(newplotdata["bid"]))
            ochl = []
            iteration = list(newplotdata["Iteration"])
            bid = list(newplotdata["bid"])
            ask = list(newplotdata["ask"])
            for lower in range(upper):
                append = iteration[lower], bid[lower], ask[lower], ask[lower], bid[lower]
                ochl.append(append)
            
            self.plotter.addcandlestick(ochl, "candlestick")
            if self.xvariable!=None and self.yvariablelist!= None:
                for index, yvariable in enumerate(self.yvariablelist):
                    self.plotter.addlineplot(newplotdata[[self.xvariable,yvariable]],"lineplot"+str(index+1), color="#FFA500")
            
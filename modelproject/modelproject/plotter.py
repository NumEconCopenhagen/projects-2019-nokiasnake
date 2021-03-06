#importing necessary libraries.
import tkinter as tk
import pandas as pd 
import numpy as np 
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_finance import candlestick_ochl

class DataPlotter:
    """Creates a figure with subplots"""
    
    def __init__(self,figure):
        """__init__ constructor for DataPlotter class

        Args:
            figure (Matplotlib Figure): matplotlib Figure to add subplots to with DataPlotter
        """
        
        self.fig = figure
        self.subplots = {}
    
    def addlineplot(self,data,plotname,**kwargs):
        """Creates a line subplot for the dataplotter figure based on the data. 1st column
        on horizontal axis, 2nd column on the vertical axis. 

        Args:
            data (Pandas DataFrame): 2-column dataframe. 
            plotname (String): Name for the subplot
            **kwargs: kwargs for the pyplot.plot method used to construct the subplot.
        """

        #Assign column name as variable
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]

        #Construct the line subplot 
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
        
        Args:
            data (Pandas DataFrame): 2-column dataframe. 
            plotname (String): Name for the subplot
        """
        #constructing the candlestick plot
        currentplot = self.fig.add_subplot(1,1,1)
        candlestick_ochl(currentplot,data,colorup="g")
        currentplot.set_xlabel("Iteration")
        currentplot.grid(True)

        #Add the subplot to the subplot dictionary
        self.subplots[plotname]=currentplot
    
    def figuretitle(self, figuretitle):
        """Sets the figure title

        Args:
            figuretitle (string): desired name of the figure
        """
        #set figure suptitle
        self.fig.suptitle(figuretitle)

    def clearplots(self):
        """Clear the figure and subplots"""
        #clearing figure and subplot dictionary
        self.fig.clear()
        self.subplots.clear()



class PlotterWindow:
    """Create a tk window containing a figure created with DataPlotter"""

    def __init__(self, data, slicename, graphtype, xvariable=None, yvariablelist=None, xsize=1280, ysize=720):
        """__init__ constructor for PlotterWindow class

        Args:
            data (Pandas Dataframe): Dataframe used to create the plots
            slicename (string): name of column used to get slicekeys
            graphtype (string): graph type used to plot data. options = ("candlestick", "piplot")

            xvariable (string): name of column used as x variable in plot. Default None
            yvariablelist (list of strings): name/s of column/s used as y variable/s in plot. Default None
            xsize (int): Define width of tk window. Default 1280
            ysize (int): Define height of tk window Default 720
        """
        
        self.xsize = xsize
        self.ysize = ysize
        self.data = data
        self.xvariable = xvariable
        self.yvariablelist = yvariablelist
        self.graphtype = graphtype
        self.slicename = slicename

        #create the tk window
        self.window = tk.Tk()

        #stringvar for graphmenu
        self.currentslicekey = tk.StringVar()

        #get slicekeys from slicename column
        self.slicekeys = (self.data[self.slicename].unique())

        #Create frame in self.window for graphmenu and graphnamelabel
        self.graphmenuframe = tk.Frame(self.window)

        #create graphmenu and label
        self.graphmenu = tk.OptionMenu(self.graphmenuframe, 
                    self.currentslicekey, *self.slicekeys, 
                    command = lambda x: self._ongraphmenuchange())

        self.graphnamelabel = tk.Label(self.graphmenuframe, text=self.slicename+"=")
        #pack graphmenu and label
        self.graphnamelabel.pack(side=tk.LEFT)
        self.graphmenu.pack(side=tk.LEFT)
        #pack graphmenuframe
        self.graphmenuframe.pack()

        #create Figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self.window)

        #add toolbar to canvas
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)

        #pack canvas in self.window
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand = True)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH, expand = True)
        
        #set window size
        self.window.geometry(str(self.xsize) + "x" + str(self.ysize))

        #call instance of DataPlotter
        self.plotter = DataPlotter(self.figure)

    def start(self):
        """Start the PlotterWindow"""
        self.window.mainloop()
    
    def _ongraphmenuchange(self):
        #Private method. Calls _updateplotter function and draws canvas in self.window
        
        #call _updateplotter function
        self._updateplotter(self.currentslicekey.get())
        
        #draw canvas
        self.canvas.draw()

    def _updateplotter(self, graphnamekey):
        #Private method. Clears self.figure and add new subplots to self.figure.

        #clear figure
        self.plotter.clearplots()
        #set title
        self.plotter.figuretitle(graphnamekey)

        #slice data based on graphnamekey 
        newplotdata = self.data.loc[self.data[self.slicename] == graphnamekey,:]

        #creates a linesubplot for each entry in yvariablelist
        if self.graphtype=="piplot":
            for index, yvariable in enumerate(self.yvariablelist):
                self.plotter.addlineplot(newplotdata[[self.xvariable,yvariable]], "plot"+str(index+1))
        
        #creates a candlestick plot. Section is specifically made for the
        #pirunmerged dataframe in modelprojekt.ipynb.
        if self.graphtype=="candlestick":
            #define lower and upper range
            lower = 0
            upper = len(list(newplotdata["bid"]))

            #create lists
            ochl = []
            iteration = list(newplotdata["Iteration"])
            bid = list(newplotdata["bid"])
            ask = list(newplotdata["ask"])

            #create a list of tuples
            for lower in range(upper):
                append = iteration[lower], bid[lower], ask[lower], ask[lower], bid[lower]
                ochl.append(append)
            
            #create candlestick plot from ochl list
            self.plotter.addcandlestick(ochl, "candlestick")

            #add lineplot to figure if specified
            if self.xvariable!=None and self.yvariablelist!= None:
                for index, yvariable in enumerate(self.yvariablelist):
                    self.plotter.addlineplot(newplotdata[[self.xvariable,yvariable]],"lineplot"+str(index+1), color="#FFA500")
            
#importing necessary libraries.
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
    
    def addtwinxlineplot(self, data, plotname, color="b"):
        """Create a line subplot on the secondary y-axis in the DataPlotter figure.

        Args:
            data (Pandas DataFrame): 2-column dataframe. 
            plotname (String): Name for the subplot
            color (string): Color of lineplot. Default b
        """
        
        #Assign column name as variable
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]

        #Construct the line subplot
        currentplot = self.subplots[plotname].twinx()
        currentplot.plot(data[xaxisname],data[yaxisname],color=color)
        currentplot.set_ylabel(yaxisname)
        currentplot.legend()

        #Add the subplot to the subplot dictionary
        self.subplots[plotname+"twinx"]=currentplot

    def addbarplot(self,data,plotname, color="g"):
        """Create a bar subplot in the DataPlotter figure.

        Args:
            data (Pandas DataFrame): 2-column dataframe. 
            plotname (String): Name for the subplot
            color (string): Color of lineplot. Default g
        """

        #Assign column name as variable
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]

        #Construct the bar plot 
        currentplot = self.fig.add_subplot(1,1,1)
        currentplot.bar(data[xaxisname],data[yaxisname],color=color)
        currentplot.set_xlabel(xaxisname)
        currentplot.set_ylabel(yaxisname)

        #Add the subplot to the subplot dictionary
        self.subplots[plotname]=currentplot
    
    def addsplitbarplot(self,data,plotname):
        """Create a custom bar subplot in the DataPlotter figure.

        Args:
            data (Pandas DataFrame): 2-column dataframe. 
            plotname (String): Name for the subplot
        """
        #Assign column name as variable
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]
        
        #split data[yaxisname] into two new dataframes.
        positive = data[yaxisname].copy()
        negative = data[yaxisname].copy()

        #Create NaN values based on criteria
        positive[positive<=0] = np.nan
        negative[negative> 0] = np.nan

        #Construct two bar plots based on the split data sets 
        currentplot = self.fig.add_subplot(1,1,1)
        currentplot.bar(data[xaxisname],positive,color="g")
        currentplot.bar(data[xaxisname],negative,color="r")
        currentplot.set_xlabel(xaxisname)
        currentplot.set_ylabel(yaxisname)
        currentplot.axhline(y=0,color="k")
        
        #add the subplot to the subplot dictionary
        self.subplots[plotname]=currentplot

    def figuretitle(self, figuretitle):
        """Sets the figure title

        Args:
            figuretitle (string): desired name of the figure
        """
        #set figure subtitle
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
            graphtype (string): graph type used to plot data. options = (standard)

            xvariable (string): name of column used as x variable in plot. Default None
            yvariablelist (list of strings): name/s of column/s used as y variable/s in plot. Max 3 entries. Default None
            xsize (int): Define width of tk window. Default 1280
            ysize (int): Define height of tk window Default 720
        """
        
        #attributes
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
        self.slicekeys = sorted((self.data[self.slicename].unique()))

        #Create frame in self.window for graphmenu and graphnamelabel
        self.graphmenuframe = tk.Frame(self.window)

        #create graphmenu and label
        self.graphmenu = tk.OptionMenu(self.graphmenuframe, 
                    self.currentslicekey, *self.slicekeys, 
                    command = lambda x: self._ongraphmenuchange())

        self.graphnamelabel = tk.Label(self.graphmenuframe, text="Pi=")
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
        
        #create standard plot
        if self.graphtype=="Standard":
            self.plotter.addsplitbarplot(newplotdata[[self.xvariable, self.yvariablelist[0]]],"plot1")

            if len(self.yvariablelist)>1:
                self.plotter.addtwinxlineplot(newplotdata[[self.xvariable, self.yvariablelist[1]]],"plot1")

            if len(self.yvariablelist)>2:
                self.plotter.addtwinxlineplot(newplotdata[[self.xvariable, self.yvariablelist[2]]],"plot1")
#import several libraries need for the program to function. 
import tkinter as tk
from tkinter import ttk
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pydst

#set the default language for the DST API
Dst = pydst.Dst(lang='en')

#Text fonts later referenced in the code
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana",9)
SMALL_FONT = ("Verdana",8)

#We create several global variables which will be referenced and changed.
metadatadictionary = {}
apidictionary = {}
tableid = "empty"
dataset = pd.DataFrame
datasetpivot = pd.DataFrame

#We create the main class, which defines the container in which all frames are defined. Think of it as the app itself.
class NokiaSnakeClient(tk.Tk):

    #defining the initialization method with room for the inherited args and kwargs from tk.Tk
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #We set the icon and title for the app frame
        tk.Tk.iconbitmap(self, "./Project/snakeicon.ico")
        tk.Tk.wm_title(self, "NokiaSnake client")

        #defining the container later used to create the frames in the app
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #We define the dictionary, which will be updated to contain our frames.
        self.frames = {}

        #Using a for loop, we create all the frames with the container previously defined
        for F in (PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        #We set the default frame to be PageOne
        self.show_frame(PageOne)
    #We create a function which shows the frame called in the "cont" argument
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    #The clearall function resets all global variables to their default value and shows the frame defined in the "cont" argument
    def clearall(self, cont):
        global metadatadictionary
        metadatadictionary = {} 
        global apidictionary
        apidictionary = {}
        global tableid
        tableid = "empty"
        global dataset
        dataset = pd.DataFrame
        global datasetpivot
        datasetpivot = pd.DataFrame

        frame = self.frames[cont]
        frame.tkraise()

#Creating the PageOne class, which is our startpage.
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Creating the pagetitle
        pagetitle = tk.Label(self, text = "Choosing Dataset", font = LARGE_FONT)
        pagetitle.pack(pady=10,padx=10)

        #We define a function next page, which raises different pages depending on the value of the menuvariable
        def nextpage():
            if menuvariable.get()==0:
                controller.show_frame(PageThree)
            else:
                controller.show_frame(PageTwo)

        #We create two buttons on pageone. The first runs the function nextpage.
        nextbutton = ttk.Button(self, text = "Next Page", command = nextpage)
        nextbutton.place(x=1180,y=680)
        #The second runs the function clearall defined in the class NokiaSnake_client
        clearallbutton = ttk.Button(self, text = "Clear All", command = lambda: controller.clearall(PageOne))
        clearallbutton.place(x=20, y=650)
        
        
        #Menuvariable is created as an tkinter integer variable.
        menuvariable = tk.IntVar()
        menuvariable.set(1)
        #the labels used to create the radiobutton menu is created, and we create a menu label
        menubuttonlabels = ["NAN1", "Custom data"]
        tk.Label(self, text="Choose Dataset to be used", justify = tk.LEFT, padx = 20).place(x=550, y=180)

        #We define the function loaddataset, which depending on the menubutton selected raises either the default dataset
        #or the window for custom dataset
        def LoadDataset():
            if menuvariable.get()==0:
                global dataset
                dataset = Dst.get_data(table_id = "NAN1", variables={'TRANSAKT': ["*"], 'PRISENHED': ["*"], 'Tid': ["*"]}, lang="en")

            else:
                popupmsg()

        #using a for loop we create the radiobutton menu from the label list
        for index, label in enumerate(menubuttonlabels):
            ttk.Radiobutton(self, text=label, variable=menuvariable, command = LoadDataset,
                value=index).place(x=600, y=200+index*20)
        
        
        #We define the function popupmsg, which creates a popupwindow.   
        def popupmsg():
            popup = tk.Tk()
            #We set the window titel and create a warning label.
            popup.wm_title("Load dataset")
            label = ttk.Label(popup, text="Warning: Experimental Feature", font=NORM_FONT)
            label.place(x=0,y=0)      

            #We create a entry field, which is used to enter the name of a table from DST.
            entry1 = tk.Entry(popup)
            entry1.place(x=38,y=50)

            #we define the function loadcustomdata. The function takes the text from the entry field tries to use it
            #for the DST api to retrieve metadata about a table.
            def loadcustomdata():
                #we call global in order to save the changes to the variable.               
                global tableid
                #we retrieved the text from the entryfield
                tableid = entry1.get()
                #We try to run tableid in the API
                try:
                    #we pull metadata from the api and create the list text which contains the category titles
                    data = Dst.get_variables(table_id=tableid)
                    categories = list(data["text"])
                    
                    #The for loop access the metadata from the api and appends the found information to the metadatadictionary
                    #and the apidictionary
                    for title in categories:
                        dataframe = data.loc[data["text"] == title,"values"]
                        data_list = list(dataframe)
                        dict_list = []
                        for sublist in data_list:
                            for dic in sublist:
                                dict_list.append(dic)
                        metadatadictionary.update({title: dict_list})
                    for title in categories:
                        api_id = data.loc[data["text"]== title, "id"].item()
                        apidictionary.update({title: api_id})
                    #close the window
                    popup.destroy()
                #if the text entered in the entry field does not correspond to a table in the api, we raise an error message
                except:
                    errormessage = ttk.Label(popup, foreground = "red", text="Table not found", font=NORM_FONT)
                    errormessage.place(x=42,y=70)

            #We create the button which executes the function loadcustomdata
            button = tk.Button(popup, text="Load", command = loadcustomdata)
            button.place(x=80,y=120)
            #we set the default size for the popup window and run it with mainloop()
            popup.geometry("200x150")
            popup.mainloop()        


#We define the class for pagetwo, which is raised if the custom dataset was loaded.
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #creating the title label
        titlelabel = tk.Label(self, text = "Customize Dataset", font=LARGE_FONT)
        titlelabel.pack(pady=10,padx=10)
        
        #Navigation button which brings you back to pageone
        button1 = ttk.Button(self, text = "Back", command = lambda: controller.show_frame(PageOne))
        button1.place(x=20, y=680)
        
        #clearallbutton identical to the one from pageone
        clearallbutton = ttk.Button(self, text = "Clear All", command = lambda: controller.clearall(PageOne))
        clearallbutton.place(x=20, y=650)

        #we define the function getdataset. The function retrives the data set specified by your choices made on the page.
        def getdataset():
            selectedvariables = {}
            #the for loop uses the information stored in the selectedbutton dictionary to create the selectedvariables dictionary
            #through reference to the metadatadictionary and apidictionary
            for header, elist in metadatadictionary.items():
                list1 = []
                for key in selectedbutton:
                    if selectedbutton[key].get():
                        list1.append(key)
                list2 = []
                for dic in elist:
                    if dic["text"] in list1:
                        list2.append(dic["id"])
                if list2 != []:
                    selectedvariables.update({str(apidictionary[header]): list2})    
            #We call global to change the dataset dataframe.
            global dataset
            dataset = Dst.get_data(table_id=tableid, variables = selectedvariables)
        
        #button which runs the getdataset function    
        getdatabutton = ttk.Button(self, text = "Get Data", command = getdataset)
        getdatabutton.place(x=600,y=650)
        
        #We define a function to save the dataset as an xlsx file in the folder the program is running from
        def savedataset():
            savepath = "./"+str(tableid)+".xlsx"
            dataset.to_excel(savepath, sheet_name="Sheet1")
        #button which runs the savedataset function
        savedatabutton = ttk.Button(self, text = "Save Data", command = savedataset)
        savedatabutton.place(x=600,y=680)
        
        #We define the dictionary selectedbutton, which we will populate with the generate function
        selectedbutton = {}
        
        #The generate function generates several interior frames on the page, which contains lists of chechbuttons.
        #The id on the buttons are added to the selectedbutton dictionary when the button is pressed.
        def generate():
            for index, header in enumerate(metadatadictionary):
                #the if has no purpose but to help place the generated frames on the row below, when more than 4 frames
                #are generated. The functions in if/else are identical except the .place(x,y)
                if index > 3:
                    #create a label for the list frame
                    label = tk.Label(self, text = header, font = SMALL_FONT)
                    label.place(x=50+290*(index-4), y=360)
                    #create the list frame from the ScrollableFrame class, which is defined later.
                    checkboxlist_index = ScrollableFrame(self)
                    checkboxlist_index.place(x=50+290*(index-4), y=380)
                    #for loop is used to populate the list frame with checkboxes.
                    for index, value in enumerate(metadatadictionary[header]):
                        is_selected = tk.BooleanVar()
                        ttk.Checkbutton(checkboxlist_index.interior, text=value["text"], variable=is_selected).grid(row=index,column=0,sticky="W")
                        selectedbutton[value["text"]] = is_selected
                #See the if explanation
                else:
                    label = tk.Label(self, text = header, font = SMALL_FONT)
                    label.place(x=50+290*index, y=80)
                    checkboxlist_index = ScrollableFrame(self)
                    checkboxlist_index.place(x=50+290*index,y=100)

                    for index, value in enumerate(metadatadictionary[header]):
                        is_selected = tk.BooleanVar()
                        ttk.Checkbutton(checkboxlist_index.interior, text=value["text"], variable=is_selected).grid(row=index,column=0,sticky="W")
                        selectedbutton[value["text"]] = is_selected
        #button which runs the generate function
        button3 = ttk.Button(self, text = "generate lists", command = generate)
        button3.place(x=50,y=50)


#We define the class pagethree, which contains the analysis of the default dataset.
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #creating the pagetitle label
        Pagetitle = tk.Label(self, text = "NAN1 Table from DST", font = LARGE_FONT)
        Pagetitle.pack(pady=10,padx=10)
        #create a label to help find the make graph buttons
        graphlabel = tk.Label(self, text = "Create Graph", font = NORM_FONT)
        graphlabel.place(x=825,y=70)
        
        #creating a button, which brings you back to pageone
        button1 = ttk.Button(self, text = "Back", command = lambda: controller.show_frame(PageOne))
        button1.place(x=20, y=680)
        
        #clearallbutton as previously defined
        clearallbutton = ttk.Button(self, text = "Clear All", command = lambda: controller.clearall(PageOne))
        clearallbutton.place(x=20, y=650)

        #creating a variable and dictionary which is used in the generate2 function
        buttonvariable = tk.StringVar()
        selected = {}
        
        #This generate function acts as the last. We create 2 frames and populate one with radiobuttons and the other with
        #checkboxes. 
        def generate2():
            #label for the frame
            pricelabel = tk.Label(self, text="Price Unit", font = SMALL_FONT)
            pricelabel.place(x=50, y=50)
            #creating the frame with the scrollableframe class
            prislist_index = ScrollableFrame(self)
            prislist_index.place(x=50, y=70)
            #populate frame with buttons
            for index, titel in enumerate(dataset["PRISENHED"].unique()):
                ttk.Radiobutton(prislist_index.interior, text=titel, variable=buttonvariable, value=titel).grid(row=index, column=0, sticky="w")
            
            #label for the frame
            translabel = tk.Label(self, text="Transaction", font = SMALL_FONT)
            translabel.place(x=300, y=50)
            #creating the frame with the scrollableframe class
            translist_index = ScrollableFrame(self)
            translist_index.place(x=300,y=70)
            #populating the frame with buttons
            for index, titel in enumerate(dataset["TRANSAKT"].unique()):
                is_selected = tk.BooleanVar()
                tk.Checkbutton(translist_index.interior, text=titel, variable=is_selected).grid(row=index,column=0,sticky="W")
                selected.update({titel: is_selected})
        #button for running the generate2 function
        generatebutton = ttk.Button(self, text = "generate lists", command = generate2)
        generatebutton.place(x=50,y=20)
        
        #we create a textwindow from the scrollableframe class, which we use to display dataset statistics
        textwindow = ScrollableFrame(self)
        textwindow.place(x=550,y=360)
        #creating the text widget within the frame.
        text = tk.Text(textwindow.interior, wrap="none", borderwidth=0)
        text.pack(expand=True, fill="both")

        #the function slicedata changes the NAN1 dataset based on the buttons pressed.
        def slicedata():
            #we access the global variable
            global datasetpivot
            #We reset the dataset datasetpivot, so we can run the function multiple times without saving the previous version
            datasetpivot = pd.DataFrame
            
            #we generate a list based on the checkbuttons pressed in the transaction frame
            rows = []
            for key in selected:
                if selected[key].get()==True:
                    rows.append(key)

            #based on the list rows and the buttonvariable from the price frame, we slice the dataset
            datasetsort = dataset.loc[dataset["TRANSAKT"].isin(rows)]
            datasetsort1 = datasetsort[datasetsort["PRISENHED"]==buttonvariable.get()]
            #the dataset naturally have the value row as strings when loading from the api. We change it back to integers
            datasetsort1["INDHOLD"]=pd.to_numeric(datasetsort1["INDHOLD"], errors="coerce")
            #We remove rows containing NaN in the value column.
            datasetsort1.dropna(inplace=True)
            
            #we create the datasetpivot as a wide dataframe
            datasetpivot = datasetsort1.pivot(index="TID", columns="TRANSAKT", values = "INDHOLD")
            
            #We clear the textbox frame
            text.delete('1.0', tk.END)
            #and then add some statistics about datasetpivot
            text.insert(tk.END, datasetpivot.describe())
            #the textbox is somewhat buggy and may not function, so we include the print function below for reference.
            print(datasetpivot.describe())

        #the slicebutton runs the slicedata function    
        slicebutton = ttk.Button(self, text = "slice dataset", command = slicedata)
        slicebutton.place(x=400, y=320)
        
        #we create a list of names corresponding to the plots we wish to make
        graphtypes = ["line", "stacked area", "pct. stacked area"]
        
        #we create a variable for our graph menu and set a default value
        graphmenuvariable = tk.StringVar()
        graphmenuvariable.set(graphtypes[0])

        #we create the graph menu, which is a dropdown radiobutton style menu.
        graphmenu = tk.OptionMenu(self, graphmenuvariable, *graphtypes)
        graphmenu.place(x=900,y=100)

        #The function makegraph produces a graph corresponding to your choice in the graphmenu
        def makegraph():
            #if line was chosen, create line plot
            if graphmenuvariable.get()=="line":
                datasetpivot.plot(kind="line")
                plt.ylabel(buttonvariable.get())
                plt.xlabel("Time")
                plt.show()
            #elif stacked area  was chosen, create stacked area plot
            elif graphmenuvariable.get()=="stacked area":
                datasetpivot.plot.area()
                plt.ylabel(buttonvariable.get())
                plt.xlabel("Time")
                plt.show()
            #elif percent stacked area was chosen, create such a plot
            elif graphmenuvariable.get()=="pct. stacked area":
                datasetpivot_pct = datasetpivot.divide(datasetpivot.sum(axis=1), axis=0)
                datasetpivot_pct.plot.area()
                plt.ylabel("percent")
                plt.xlabel("Time")
                plt.show()            
        
        #Create a button to run the makegraph function and create some beatiful graphs
        button = ttk.Button(self, text="Make Graph", command=makegraph)
        button.place(x=810,y=105)     


#The class scrollableframe is called to create an empty frame with scrollbars.
class ScrollableFrame(tk.Frame):
    def __init__(self, master,**kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        #note, self references to the class itself and saves the following under the class.
        #define the vertical scrollbar
        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(side='right', fill="y",  expand="false")
        #define the horizontal scrollbal
        self.hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hscrollbar.pack(side='bottom', fill="x",  expand="false")

        #create the canvas for the class
        self.canvas = tk.Canvas(self, width=200, height=220, yscrollcommand=self.vscrollbar.set,
                                xscrollcommand=self.hscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand="true")

        #configuring the function of the scrollbars
        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

        #create a frame inside the canvas, which the scrollbars scroll around within the canvas. Think of the canvas
        #as a glimpse at some of the frame
        self.interior = tk.Frame(self.canvas, **kwargs)
        self.canvas.create_window(0, 0, window=self.interior, anchor="nw")
        self.bind("<Configure>", self.set_scrollregion)
    #defining the scrollregion function, which sets the frame as scrollable region within the canvas    
    def set_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    
#After defining all our classes, we set the NokiaSnakeClient class as our app. We adjust the default size 
#and run it with mainloop
app = NokiaSnakeClient()
app.geometry("1280x720")
app.mainloop()
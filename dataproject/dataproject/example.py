#import packages
from tkinter import *
from PIL import Image, ImageTk

#starting the main window.
class Window(Frame):
    #Defining the window
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()
    
    
    #The window itself
    def init_window(self):
        self.master.title("GUI")

        self.pack(fill=BOTH, expand=1)
      
        #button
        button = Button(self, text="Show best game", command=self.showImg)
        button.place(x=150,y=500)

    def showImg(self):
        load = Image.open("dataproject\dataproject\snake.png")
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=40,y=0)


#determine default size of window and running it
root=Tk()
root.geometry("400x600")
app = Window(root)
root.mainloop()

from pickletools import uint8
from re import I
import sys
import tkinter
from tkinter import Frame, Tk, BOTH, Text, Menu, END,Button,Label,Scale,DoubleVar
from tkinter.filedialog import Open, SaveAs
import cv2
import numpy as np
class Main(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.alpha = DoubleVar()
        self.beta = DoubleVar()
        self.initUI()
  
    def initUI(self):
        self.parent.title("Digital Image Processing")
        self.pack(fill=BOTH, expand=1)
  
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
  
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open Image1", command=self.onOpen1)
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)
         
        # label for the slider
        slider_label = Label(
            self.parent,
            text='Contrast:'
        )

        slider_label.place(x=10,y=50)

        #  slider
        slider =Scale(
            self.parent,
            from_=1,
            to=3,
            resolution = 1,
            orient='horizontal',  # vertical
            variable=self.alpha,
            command=self.enhancement
        )

        slider.place(x=100,y=50)
        
         # label for the slider
        slider_label2 = Label(
            self.parent,
            text='Brightness:'
        )

        slider_label2.place(x=10,y=100)

        #  slider
        slider2 =Scale(
            self.parent,
            from_=0,
            to=100,
            resolution = 1,
            orient='horizontal',  # vertical
            variable=self.beta,
            command=self.enhancement
        )

        slider2.place(x=100,y=100)
 

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
  
    def onOpen1(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        fl = dlg.show()
  
        if fl != '':
            global imgin
            imgin = cv2.imread(fl)
            # imgin = cv2.imread(fl,cv2.IMREAD_COLOR);
            cv2.namedWindow("ImageIn 1", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("ImageIn 1", imgin)
      
    def onSave(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = SaveAs(self,filetypes = ftypes);
        fl = dlg.show()
        if fl != '':
            cv2.imwrite(fl,imgout)
            
    
    def enhancement(self,event):
        global imgout
        #imgout = cv2.convertScaleAbs(imgin,alpha=self.alpha.get(),beta=self.beta.get())
        imgout = imgin*self.alpha.get() + self.beta.get()
        imgout[imgout>255] = 255
        imgout[imgout<0]=0
        imgout = imgout.astype(np.uint8)
        cv2.imshow("IMG",imgout)


root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


from random import randint
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
        self.value = [randint(0, 255), randint(0, 255), randint(0, 255)]
        self.initUI()
  
    def initUI(self):
        self.parent.title("Digital Image Processing")
        self.pack(fill=BOTH, expand=1)
  
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
  
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open Image1", command=self.onOpen)
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        btn1 = Button(self.parent, text = 'Padding CLAMP', bd = '7',
                          command = self.onClickClamp )
        btn1.place(x=10, y=50)
        
        
        btn2 = Button(self.parent, text = 'Padding ZERO', bd = '7',
                          command = self.onClickZero )
        btn2.place(x=120, y=50)
        btn3 = Button(self.parent, text = 'Padding CONSTANT', bd = '7',
                          command = self.onClickConstant )
        btn3.place(x=230, y=50)
        btn4 = Button(self.parent, text = 'Padding WRAP', bd = '7',
                          command = self.onClickWrap )
        btn4.place(x=10, y=120)
        btn5 = Button(self.parent, text = 'Padding REFLECT', bd = '7',
                          command = self.onClickReflect)
        btn5.place(x=120, y=120)
        
 
# Set the position of button on the top of window.  

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
  
    def onOpen(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        fl = dlg.show()
  
        if fl != '':
            global imgin
            imgin = cv2.imread(fl,cv2.COLOR_BGR2GRAY)
            cv2.namedWindow("ImageIn 1", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("ImageIn 1", imgin)
         

    def onSave(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = SaveAs(self,filetypes = ftypes);
        fl = dlg.show()
        if fl != '':
            cv2.imwrite(fl,imgout)
    def onClickClamp(self):
        self.Padding(cv2.BORDER_REPLICATE)
    def onClickConstant(self):
        self.value = [randint(0, 255), randint(0, 255), randint(0, 255)]
        self.Padding(cv2.BORDER_CONSTANT)
        
    def onClickZero(self):
        self.value = [0,0,0]
        self.Padding(cv2.BORDER_CONSTANT)
        
    def onClickReflect(self):
        self.Padding(cv2.BORDER_REFLECT)
    def onClickWrap(self):
        self.Padding(cv2.BORDER_WRAP)
    def Padding(self, borderType):
        global imgout
        global imgin
        top = bottom = left =right = padding = 40
        M,N = imgin.shape[0],imgin.shape[1]
        
        imgout = cv2.copyMakeBorder(imgin,top,bottom,left,right,borderType,None,self.value)
        cv2.imshow("ImgOut", imgout)
                
        


root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


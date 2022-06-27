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
        self.current_value = DoubleVar()
        self.initUI()
  
    def initUI(self):
        self.parent.title("Digital Image Processing")
        self.pack(fill=BOTH, expand=1)
  
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
  
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open Image1", command=self.onOpen1)
        fileMenu.add_command(label="Open Image2", command=self.onOpen2)
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        btn = Button(self.parent, text = 'Click me !', bd = '5',
                          command = self.onClickBlending )
        
        
        # label for the slider
        slider_label = Label(
            self.parent,
            text='Slider:'
        )

        slider_label.place(x=10,y=50)

        #  slider
        slider =Scale(
            self.parent,
            from_=0,
            to=1,
            resolution = 0.1,
            orient='horizontal',  # vertical
            variable=self.current_value
        )

        slider.place(x=100,y=50)
 
# Set the position of button on the top of window.  
        btn.place(x=150,y=100)

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
  
    def onOpen1(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        fl = dlg.show()
  
        if fl != '':
            global imgin1
            imgin1 = cv2.imread(fl)
            # imgin = cv2.imread(fl,cv2.IMREAD_COLOR);
            cv2.namedWindow("ImageIn 1", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("ImageIn 1", imgin1)
            
    def onOpen2(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        fl = dlg.show()
  
        if fl != '':
            global imgin2
            imgin2 = cv2.imread(fl)
            # imgin = cv2.imread(fl,cv2.IMREAD_COLOR);
            cv2.namedWindow("ImageIn 2", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("ImageIn 2", imgin2)

    def onSave(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = SaveAs(self,filetypes = ftypes);
        fl = dlg.show()
        if fl != '':
            cv2.imwrite(fl,imgout)
            
    def onClickBlending(self):
        print(self.current_value.get())
        self.blending(imgin1,imgin2,self.current_value.get())
    
    def blending(self, img1,img2,alpha):
        global imgout
        imgout = ((1-alpha)*img1 + alpha*img2).astype("uint8")
        cv2.imshow("Blending Img",imgout)
        


root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


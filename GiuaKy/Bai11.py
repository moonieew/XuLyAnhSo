
import math
from scipy import ndimage
import tkinter
from tkinter import Frame, Tk, BOTH, Text, Menu, END,Button,Label,Scale,DoubleVar,IntVar
from tkinter.filedialog import Open, SaveAs
import cv2
import numpy as np
class Main(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.kernel = IntVar()
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
        
        
        # label for the slider
        slider_label = Label(
            self.parent,
            text='Kernel:'
        )

        slider_label.place(x=10,y=50)

        #  slider
        slider =Scale(
            self.parent,
            from_=1,
            to=20,
            resolution = 1,
            orient='horizontal',  # vertical
            variable=self.kernel,
            command=self.onChangeKernel
        )

        slider.place(x=100,y=50)
 
# Set the position of button on the top of window.  

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
  
    def onOpen(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        fl = dlg.show()
  
        if fl != '':
            global imgin
            imgin = cv2.imread(fl)
            # imgin = cv2.imread(fl,);
            cv2.namedWindow("ImageIn 1", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("ImageIn 1", imgin)
            self.onChangeKernel(None)
         

    def onSave(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = SaveAs(self,filetypes = ftypes);
        fl = dlg.show()
        if fl != '':
            cv2.imwrite(fl,imgout)
        
    def onChangeKernel(self,event):
        global imgout
        pix_blur = (self.kernel.get(),self.kernel.get())
        kernel = np.ones(pix_blur) / float(pix_blur[0]*pix_blur[1])
        
        img_B,img_G,img_R = cv2.split(imgin)
        img_gauss_B = ndimage.convolve(img_B, kernel, mode='mirror')
        img_gauss_G = ndimage.convolve(img_G, kernel, mode='mirror')
        img_gauss_R = ndimage.convolve(img_R, kernel, mode='mirror')
        imgout= cv2.merge([img_gauss_B,img_gauss_G,img_gauss_R])
        cv2.imshow("Gaussian Blur Image",imgout) 
               

root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


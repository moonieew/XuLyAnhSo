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
        
        btn1 = Button(self.parent, text = 'Equalize histogram', bd = '5',
                          command = self.onClickEqual_his )
        btn1.place(x=200, y=100)
        

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
  
    def onOpen(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        fl = dlg.show()
  
        if fl != '':
            global imgin
            imgin = cv2.imread(fl,cv2.IMREAD_GRAYSCALE)
            cv2.namedWindow("ImageIn 1", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("ImageIn 1", imgin)
         

    def onSave(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = SaveAs(self,filetypes = ftypes);
        fl = dlg.show()
        if fl != '':
            cv2.imwrite(fl,imgout)
    def create_histogram(self,img):
        assert len(img.shape) == 2 # check grayscale image
        histogram = [0] * 256 # list of intensity frequencies, 256 zero values
        for row in range(img.shape[0]): # traverse by row (y-axis)
            for col in range(img.shape[1]): # traverse by column (x-axis)
                histogram[img[row, col]] += 1
        return histogram
    def equalize_histogram(self,img, histogram):
        # build H', cumsum
        new_H = [0] * 257
        for i in range(0, len(new_H)):
            new_H[i] = sum(histogram[:i])
        new_H = new_H[1:]
        
        
        # scale H' to [0, 255]
        max_value = max(new_H)
        min_value = min(new_H)
        new_H = [int(((f-min_value)/(max_value-min_value))*255) for f in new_H]
        
        
        # apply H' to img
        for row in range(img.shape[0]): # traverse by row (y-axis)
            for col in range(img.shape[1]): # traverse by column (x-axis)
                img[row, col] = new_H[img[row, col]]
        return img
    
    def onClickEqual_his(self):
        global imgout
        histogram = self.create_histogram(imgin)
        imgout = self.equalize_histogram(imgin,histogram)
        
        cv2.imshow("Equalized Image",imgout) 
               


root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


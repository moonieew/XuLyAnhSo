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
                          command = self.onClickDistance )
        btn1.place(x=200, y=100)
        
        
 
# Set the position of button on the top of window.  

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
    
    def dt_1d(self,dataInput, n):
        output = np.zeros(dataInput.shape)
        k = 0
        v = np.zeros((n,))
        z = np.zeros((n + 1,))
        v[0] = 0
        z[0] = -np.inf
        z[1] = +np.inf
        for q in range(1, n):
            s = (((dataInput[q] + q * q) - (dataInput[v[k]] + v[k] * v[k])) / (2.0 * q - 2.0 * v[k]))
            while s <= z[k]:
                k -= 1
                s = (((dataInput[q] + q * q) - (dataInput[v[k]] + v[k] * v[k])) / (2.0 * q - 2.0 * v[k]))
            k += 1
            v[k] = q
            z[k] = s
            z[k + 1] = +np.inf

        k = 0
        for q in range(n):
            while z[k + 1] < q:
                k += 1
            value = ((q - v[k]) * (q - v[k]) + dataInput[v[k]])
            if value > 255: value = 255
            if value < 0: value = 0
            output[q] = value
        return output

    def dt_2d(self,dataInput):
        height, width = dataInput.shape
        f = np.zeros(max(height, width))
        for x in range(width):
            f = dataInput[:,x]
            dataInput[:,x] = self.dt_1d(f, height)
        for y in range(height):
            f = dataInput[y,:]
            dataInput[y,:] = self.dt_1d(f, width)
        return dataInput
    
    def chamfer_distance(self,img):
        w, h = img.shape
        dt = np.zeros((w,h), np.uint32)
        x = 0
        y = 0
        if img[x,y] == 0:
            dt[x,y] = 65535 
        for x in range(1, w):
            if img[x,y] == 0:
                dt[x,y] = 3 + dt[x-1,y]
        for y in range(1, h):
            x = 0
            if img[x,y] == 0:
                dt[x,y] = min(3 + dt[x,y-1], 4 + dt[x+1,y-1])
            for x in range(1, w-1):
                if img[x,y] == 0:
                    dt[x,y] = min(4 + dt[x-1,y-1], 3 + dt[x,y-1], 4 + dt[x+1,y-1], 3 + dt[x-1,y])
            x = w-1
            if img[x,y] == 0:
                dt[x,y] = min(4 + dt[x-1,y-1], 3 + dt[x,y-1], 3 + dt[x-1,y])
        # Backward pass
        for x in range(w-2, -1, -1):
            y = h-1
            if img[x,y] == 0:
                dt[x,y] = min(dt[x,y], 3 + dt[x+1,y])
        for y in range(h-2, -1, -1):
            x = w-1
            if img[x,y] == 0:
                dt[x,y] = min(dt[x,y], 3 + dt[x,y+1], 4 + dt[x-1,y+1])
            for x in range(1, w-1):
                if img[x,y] == 0:
                    dt[x,y] = min(dt[x,y], 4 + dt[x+1,y+1], 3 + dt[x,y+1], 4 + dt[x-1,y+1], 3 + dt[x+1,y])
            x = 0
            if img[x,y] == 0:
                dt[x,y] = min(dt[x,y], 4 + dt[x+1,y+1], 3 + dt[x,y+1], 3 + dt[x+1,y])
        return dt
    
    def onClickDistance(self):
        global imgout
        imgout = cv2.distanceTransform(imgin,cv2.DIST_L1,maskSize=3)
        cv2.normalize(imgout, imgout, 0, 1.0, cv2.NORM_MINMAX)
        cv2.imshow("Equalized Image",imgout) 
               


root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


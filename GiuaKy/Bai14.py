
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
        self.d = IntVar(value=12)
        self.sigma = IntVar(value=16)
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
            text='D:'
        )

        slider_label.place(x=10,y=50)

        #  slider
        slider =Scale(
            self.parent,
            from_=4,
            to=30,
            resolution = 2,
            orient='horizontal',  # vertical
            variable=self.d,
            command=self.onChangeValue
        )

        slider.place(x=100,y=50)
        
         # label for the slider
        slider_label2 = Label(
            self.parent,
            text='Sigma Color/Space:'
        )

        slider_label2.place(x=10,y=100)

        #  slider
        slider2 =Scale(
            self.parent,
            from_=2,
            to=100,
            resolution = 4,
            orient='horizontal',  # vertical
            variable=self.sigma,
            command=self.onChangeValue
        )

        slider2.place(x=100,y=100)
 
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
            self.onChangeValue(None)
         

    def onSave(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = SaveAs(self,filetypes = ftypes);
        fl = dlg.show()
        if fl != '':
            cv2.imwrite(fl,imgout)
   
    def distance(self,i, j):
        return np.absolute(i-j)

    def bilateral_filter(self,i,j,d,I,sigma_d,sigma_r):
        arr=[]
        sum_num=0
        sum_den=0
        for k in range(i-math.floor(d/2),i+math.ceil(d/2)):
            for l in range(j-math.floor(d/2),j+math.ceil(d/2)):
                if k >= I.shape[0]:
                    k = k- I.shape[0]
                if l >= I.shape[1]:
                    l = l - I.shape[1]
                term1=(((i-k)**2)+(j-l)**2)/(sigma_d**2*2)
                term2=(self.distance(I[i,j],I[k,l]))/(sigma_r**2*2)
                term=term1+term2
                w=math.exp(-term)
                arr.append(w)
                sum_num=sum_num+(I[k,l]*w)
                sum_den=sum_den+w      
        return sum_num/sum_den
        
    def onChangeValue(self,event):
        global imgout
        imgout = np.copy(imgin)
        imgout = cv2.bilateralFilter(imgin,self.d.get(),self.sigma.get(),self.sigma.get())
        cv2.imshow("Bilateral Filter",imgout) 
               

np.seterr(over='ignore')
root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


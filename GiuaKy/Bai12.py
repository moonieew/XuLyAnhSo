
import math
from scipy import ndimage
import tkinter
from tkinter import Frame, Tk, BOTH, Text, Menu, END,Button,Label,Scale,DoubleVar,IntVar,Checkbutton,Radiobutton
from tkinter.filedialog import Open, SaveAs
import cv2
import numpy as np
class Main(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.sharp = IntVar(0)
        self.blur = IntVar(0)
        self.knSharp = IntVar(value=1)
        self.knBlur = IntVar(value=1)
        self.chooseBlur = IntVar(0)
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
        
        c1 = Checkbutton(self.parent, text='Apply Sharp',variable=self.sharp, onvalue=1, offvalue=0, command=self.onChangeCheck)
        c2 = Checkbutton(self.parent, text='Apply Blur',variable=self.blur, onvalue=1, offvalue=0, command=self.onChangeCheck)
        c1.place(x=10,y=50)
        c2.place(x=10,y=150)
        # label for the slider
        slider_label = Label(
            self.parent,
            text='Kernel Sharp'
        )

        slider_label.place(x=10,y=100)

        #  slider
        slider =Scale(
            self.parent,
            from_=3,
            to=25,
            tickinterval = 2,
            length=400,
            orient='horizontal',  # vertical
            variable=self.knSharp,
            command=self.onChangeValue
        )

        slider.place(x=100,y=100)
        
         # label for the slider
        slider_label2 = Label(
            self.parent,
            text='Sigma Color/Space:'
        )

        slider_label2.place(x=10,y=200)

        #  slider
        slider2 =Scale(
            self.parent,
            from_=3,
            to=25,
            tickinterval = 2,
            length=400,
            orient='horizontal',  # vertical
            variable=self.knBlur,
            command=self.onChangeValue
        )
        slider2.place(x=100,y=200)
        
        rd1= Radiobutton(root, text="Gaussian Blur", variable=self.chooseBlur, value=0,
                  command=self.onChangeBlur)
        rd2= Radiobutton(root, text="Median Blur", variable=self.chooseBlur, value=1,
                  command=self.onChangeBlur)
        rd3= Radiobutton(root, text="Bilateral Blur", variable=self.chooseBlur, value=2,
                  command=self.onChangeBlur)
        rd1.place(x=10, y=250)
        rd2.place(x=10, y=280)
        rd3.place(x=10, y=310)
 
# Set the position of button on the top of window.  

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
  
    def onOpen(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        fl = dlg.show()
  
        if fl != '':
            global imgin
            global imgout
            imgin = imgout = cv2.imread(fl)
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
   
    def unsharp_mask(self,image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
        """Return a sharpened version of the image, using an unsharp mask."""
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = float(amount + 1) * image - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if threshold > 0:
            low_contrast_mask = np.absolute(image - blurred) < threshold
            np.copyto(sharpened, image, where=low_contrast_mask)
        return sharpened
    
    def onChangeBlur(self):
        global imgout
        imgout = imgin
        kernelBlur = (self.knBlur.get(),self.knBlur.get())
        if self.sharp.get() == 1 and self.blur.get() == 1:
            imgout = self.unsharp_mask(imgout,(self.knSharp.get(),self.knSharp.get()))
            if self.chooseBlur.get() ==0:
                imgout = cv2.GaussianBlur(imgout,kernelBlur,1)
            elif self.chooseBlur.get()==1:
                imgout = cv2.medianBlur(imgout,self.knBlur.get())
            else:
                imgout = cv2.blur(imgout,kernelBlur)
        elif self.sharp.get() == 1:
            imgout = self.unsharp_mask(imgout,(self.knSharp.get(),self.knSharp.get()))
        elif self.blur.get()==1:
            if self.chooseBlur.get() ==0:
                imgout = cv2.GaussianBlur(imgout,kernelBlur,1)
            elif self.chooseBlur.get()==1:
                imgout = cv2.medianBlur(imgout,self.knBlur.get())
            else:
                imgout = cv2.blur(imgout,kernelBlur)
        
        cv2.imshow("ImgOut",imgout) 
    
    def onChangeCheck(self):
        self.onChangeBlur()
    
    def onChangeValue(self,event):
        global pastBlur,pastSharp
        
        if not self.knSharp.get() % 2:
            self.knSharp.set(self.knSharp.get()+1 if self.knSharp.get() > pastSharp else self.knSharp.get()-1)
            pastSharp = self.knSharp.get()
        if not self.knBlur.get() % 2:
            self.knBlur.set(self.knBlur.get()+1 if self.knBlur.get() > pastBlur else self.knBlur.get()-1)
            pastBlur = self.knBlur.get()
        self.onChangeBlur()
        
               
pastBlur = 3
pastSharp = 3
np.seterr(over='ignore')
root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


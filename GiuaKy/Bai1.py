
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
        self.balance = IntVar(value=1)
        self.initUI()
  
    def initUI(self):
        self.parent.title("Digital Image Processing")
        self.pack(fill=BOTH, expand=1)
  
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
  
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open Image", command=self.onOpen)
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
            to=100,
            resolution = 1,
            orient='horizontal',  # vertical
            variable=self.balance,
            command=self.onChangeBalance
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
            cv2.namedWindow("ImageIn", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("ImageIn", imgin)
            self.onChangeKernel(None)
         

    def onSave(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = SaveAs(self,filetypes = ftypes);
        fl = dlg.show()
        if fl != '':
            cv2.imwrite(fl,imgout)
            
        

    def apply_mask(self,matrix, mask, fill_value):
        masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
        return masked.filled()


    def apply_threshold(self,matrix, low_value, high_value):
        low_mask = matrix < low_value
        matrix = self.apply_mask(matrix, low_mask, low_value)

        high_mask = matrix > high_value
        matrix = self.apply_mask(matrix, high_mask, high_value)

        return matrix


    def simple_colorbalance(self,img, percent):
        """ Applies Simple Color balancing to RBG image
        Args:
        img: numpy array of an image in RGB space
        percent: [0, 100], cutoff value for light and dark pixels
        Returns:
        Color balanced image
        Examples:
        Flatten (broaden) the color histogram for a cup of coffee photo.
        >>> from skimage.data import coffee
        >>> img = coffee()
        >>> img.std().round(0)
        74.0
        >>> x = simple_colorbalance(img, 9)
        >>> x.std().round(0)
        80.0
        """
        assert img.shape[2] == 3
        assert 0 <= percent <= 100

        half_percent = percent / 200

        channels = cv2.split(img)

        out_channels = []
        for channel in channels:
            assert len(channel.shape) == 2
            # find the low and high precentile values (based on the input percentile)
            height, width = channel.shape[:2]
            vec_size = width * height
            flat = channel.reshape(vec_size)

            assert len(flat.shape) == 1

            low_val = np.percentile(flat, half_percent * 100)
            high_val = np.percentile(flat, (1 - half_percent) * 100)

            # saturate below the low percentile and above the high percentile
            thresholded = self.apply_threshold(channel, low_val, high_val)

            # scale the channel
            normalized = cv2.normalize(thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
            out_channels.append(normalized)

        return cv2.merge(out_channels)
        
    def onChangeBalance(self,event):
        global imgout
        imgout = self.simple_colorbalance(imgin,self.balance.get())
        
        cv2.imshow("Balance Color Image",imgout) 
               


root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


import sys
import tkinter
from tkinter import CENTER, Frame, Tk, BOTH, Text, Menu, END,Button,Label,Scale,IntVar
from tkinter.filedialog import Open, SaveAs
import cv2
import numpy as np
class Main(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.levelBlend = IntVar(value=1)
        self.initUI()
  
    def initUI(self):
        self.parent.title("Digital Image Processing")
        self.pack(fill=BOTH, expand=1)
  
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
  
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open Image1", command=self.onOpen1)
        fileMenu.add_command(label="Open Image2", command=self.onOpen2)
        fileMenu.add_command(label="Open Image Mask", command=self.onOpenMask)
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        btn = Button(self.parent, text = 'Blend', bd = '5',
                          command = self.blending )
        btn.place(x=200,y=100)
        slider_label = Label(
            self.parent,
            text='Level Blend:'
        )

        slider_label.place(x=10,y=50)
        slider =Scale(
            self.parent,
            from_=1,
            to=10,
            resolution = 1,
            orient='horizontal',  
            variable=self.levelBlend,
            command=self.onChangeLevelBlend
        )

        slider.place(x=100,y=50) 
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
            imgin1 = cv2.resize(imgin1, None, fx=0.5, fy=0.5)
            cv2.namedWindow("ImageIn 1", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("ImageIn 1", imgin1)
            
    def onOpen2(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        fl = dlg.show()
  
        if fl != '':
            global imgin2
            imgin2 = cv2.imread(fl)
            imgin2 = cv2.resize(imgin2, None, fx=0.5, fy=0.5)
            cv2.namedWindow("ImageIn 2", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("ImageIn 2", imgin2)
    
    def onOpenMask(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        fl = dlg.show()
  
        if fl != '':
            global imgMask
            imgMask = cv2.imread(fl)
            imgMask = cv2.resize(imgMask, None, fx=0.5, fy=0.5)
            imgMask = cv2.normalize(imgMask,None,0,1,cv2.NORM_MINMAX)
            cv2.namedWindow("Image Mask", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("Image Mask", imgMask*255)

    def onSave(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = SaveAs(self,filetypes = ftypes);
        fl = dlg.show()
        if fl != '':
            cv2.imwrite(fl,imgout)
            
        
    def pyr_up(self,p, kernel_size=(5,5)):
        M,N,C=np.shape(p)
        idx=np.arange(0,M)
        out=np.insert(p,idx,values=0,axis=0)
        idx=np.arange(0,N)
        out=np.insert(out,idx,values=0,axis=1)
        out = cv2.GaussianBlur(4*out,kernel_size,1)
        return out


    def pyr_down(self,p, kernel_size=(5,5)):
        c = cv2.GaussianBlur(p,kernel_size,1) 
        M,N,C=np.shape(c)
        idxi=0
        idxj=0
        out1=np.zeros((M//2,N,C))
        for i in range(M):
            if i%2 !=0:
                out1[idxi,:,:]=c[i,:,:]
                idxi+=1

        out=np.zeros((M//2,N//2,C))
        for j in range(N):
            if j%2 !=0:
                out[:,idxj,:]=out1[:,j,:]
                idxj+=1
        return out

    def gaussian_pyramid(self,img, num_levels):
        img = img.astype('float')
        gp=[]
        gp.append(img)
        X=gp[0]
        for i in range(num_levels):
            X=self.pyr_down(X)
            gp.append(X)
        return gp

    def laplacian_pyramid(self,gp, num_levels):
        lp=[]
        for i in range(num_levels-1):
            X=gp[i]-self.pyr_up(gp[i+1])
            lp.append(X)
            
        lp.append(gp[num_levels-1])
        return lp
    
    def reconstruct_img(self,lp):
        lp.reverse()
        recon_img=lp[0]
        
        for i in range(len(lp)-1):
            recon_img=self.pyr_up(recon_img)+lp[i+1]
        return recon_img

    def pyr_blend(self,img1, img2, mask, num_levels=6):
        gp1, gp2, gpm = self.gaussian_pyramid(img1, num_levels), self.gaussian_pyramid(img2, num_levels), self.gaussian_pyramid(mask, num_levels)
        lp1, lp2, lpm = self.laplacian_pyramid(gp1, num_levels), self.laplacian_pyramid(gp2, num_levels), self.laplacian_pyramid(gpm, num_levels)
        new_lp=[]

        for i in range(num_levels):
            X=lp1[i]*gpm[i]
            Y=lp2[i]*(1-gpm[i])
            new_lp.append((X+Y))

        img_blend=self.reconstruct_img(new_lp)
        return img_blend
    
    def onChangeLevelBlend(self,event):
        self.blending()
        
    def blending(self):
        global imgout
        global imgin1
        global imgin2
        global imgMask
        imgout = self.pyr_blend(imgin1, imgin2, imgMask, self.levelBlend.get())
        print(imgout)
        cv2.imshow("Blending Img",imgout.astype(np.uint8))
        


root = Tk()
Main(root)
root.geometry("640x480+100+100")
root.mainloop()


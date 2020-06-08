# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 17:46:08 2020

@author: Syd_R

Refrences
[1] https://www.geeksforgeeks.org/loading-images-in-tkinter-using-pil/
[2] https://www.youtube.com/watch?time_continue=675&v=Aim_7fC-inw&feature=emb_logo
[3] https://abdurrahmaanjanhangeer.wordpress.com/2017/05/07/python-tkinter-new-window-on-button-click/
[4] https://towardsdatascience.com/edge-detection-in-python-a3c263a13e03
[5] https://codeloop.org/python-opencv-circle-detection-with-houghcircles/
[6] https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
[7] https://www.life2coding.com/how-to-display-multiple-images-in-one-window-using-opencv-python/
[8] https://stackoverflow.com/questions/24274072/tkinter-pyimage-doesnt-exist
[9] https://stackoverflow.com/questions/54641616/low-pass-filter-for-blurring-an-image
"""


from tkinter import *
import tkinter as tk
#from PIL import ImageTK, Image
from PIL import Image, ImageDraw, ImageTk
from tkinter import filedialog
from collections import defaultdict
from tkinter import messagebox
import matplotlib.pyplot as plt
import cv2
import numpy as np
from urllib.request import urlopen
import io
from skimage.io import imread
from scipy import fftpack as fp
from scipy import fftpack

root = tk.Tk()
root.title("Image Processing with Python")
C = Canvas(root, bg="blue", height=100, width=400)
URL = 'https://i.pinimg.com/originals/0f/19/b2/0f19b29838a5f696f6691e8dcde89ba2.png'
my_page = urlopen(URL)
imgURL = io.BytesIO(my_page.read())
filename1= ImageTk.PhotoImage(Image.open(imgURL))
#filename1 = PhotoImage(file = 'C:/Users/Syd_R/Documents/landscape.png')
background_label = Label(root, image=filename1)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()


def open():
    global my_image
    openY=Toplevel(root)
    root.filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("image files", 
                                                        "*.jpg*"), 
                                                       ("all files", 
                                                        "*.*")))
    my_label = Label(root, text=root.filename).pack()
    my_image = ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label = Label(openY, image=my_image).pack()

    
    
my_btn = Button(root,  text="Open File",  command=open).pack(pady = 20, padx = 20)

def open1():
    global edges_img, my_img
    
    openX=Toplevel(root)
    #define the vertical filter
    vertical_filter = [[-1,-2,-1], [0,0,0], [1,2,1]]

    #define the horizontal filter
    horizontal_filter = [[-1,0,1], [-2,0,2], [-1,0,1]]

    #read in the pinwheel image
    #img = plt.imread('C:/Users/Syd_R/Documents/1.jpg')
    root.filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("image files", 
                                                        "*.jpg*"), 
                                                       ("all files", 
                                                        "*.*")))
    img1 = cv2.imread(root.filename)
    img = plt.imread(root.filename)


    #get the dimensions of the image
    n,m,d = img.shape

    #initialize the edges image
    edges_img = img.copy()

    #loop over all pixels in the image
    for row in range(3, n-2):
        for col in range(3, m-2):
        
            #create little local 3x3 box
            local_pixels = img[row-1:row+2, col-1:col+2, 0]
        
            #apply the vertical filter
            vertical_transformed_pixels = vertical_filter*local_pixels
            #remap the vertical score
            vertical_score = vertical_transformed_pixels.sum()/4
        
            #apply the horizontal filter
            horizontal_transformed_pixels = horizontal_filter*local_pixels
            #remap the horizontal score
            horizontal_score = horizontal_transformed_pixels.sum()/4
        
            #combine the horizontal and vertical scores into a total edge score
            edge_score = (vertical_score**2 + horizontal_score**2)**.5
        
            #insert this edge score into the edges image
            edges_img[row, col] = [edge_score]*3
    #remap the values in the 0-1 range in case they went out of bounds
    edges_img = edges_img/edges_img.max()
    #plt.imshow(edges_img)
    #plt.axis('off')
    #plt.show()
    edges_img = Image.fromarray((edges_img * 255).astype(np.uint8))
    edges_img.save('out.bmp')
    img_concate_Hori=np.concatenate((img1,edges_img),axis=1)
    cv2.imshow('concatenated',img_concate_Hori)
    cv2.waitKey(0)
    #my_img =  ImageTk.PhotoImage(Image.open("out.bmp"))
    #my_label = Label(openX, image=my_img).pack()    
    
my_btn1 = Button(root,  text="Detect Edges",  command=open1).pack(pady = 20, padx = 20)

def open2():
    global planets, circles
    openZ=Toplevel(root)
    
    
    #cv2.destroyAllWindows() 
    #root.filename = filedialog.askopenfilename(initialdir="C:/Users/Syd_R/Documents", title= "Select a File", filetypes= (("jpg files", "*.jpg"),("all files", "*.*")))
    root.filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("image files", 
                                                        "*.jpg*"), 
                                                       ("all files", 
                                                        "*.*")))
    planets1 = cv2.imread(root.filename)
    planets = cv2.imread(root.filename)

    gray_img	=	cv2.cvtColor(planets,	cv2.COLOR_BGR2GRAY)
    img	= cv2.medianBlur(gray_img,	5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
 
    #center
 
    circles	= cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,param1=50,param2=12,minRadius=0,maxRadius=20)
    circles	= np.uint16(np.around(circles))
 
    for	i in circles[0,:]:
	    #	draw	the	outer	circle
	    cv2.circle(planets,(i[0],i[1]),i[2],(0,255,0),6)
	    #	draw	the	center	of	the	circle
	    cv2.circle(planets,(i[0],i[1]),2,(0,0,255),3)
    img3 = cv2.hconcat([planets1,planets])
    cv2.imshow("HoughCirlces",	img3)
    cv2.waitKey()
  

my_btn2 = Button(root,  text="Hough Transform",  command=open2).pack(pady = 20, padx = 20)  
  

def open3(): 
    global  my_image1
    openV=Toplevel(root)
    #define the vertical filter
    root.filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("image files", 
                                                        "*.jpg*"), 
                                                       ("all files", 
                                                      "*.*")))
    img = cv2.imread(root.filename, cv2.IMREAD_GRAYSCALE)
    dft = np.fft.fft2(img)
    dft_shift = np.fft.fftshift(dft)
    #fft_x = np.asarray(dft_shift, dtype=np.uint8)
    fft_x = np.log10(1+abs(dft_shift))
    rescaled = 255 * (fft_x - fft_x.min()) / fft_x.ptp()
    foto = Image.fromarray(rescaled.astype(np.uint8), mode='L')
    foto = np.asarray(foto, dtype=np.uint8)
    
    (w, h) = dft_shift.shape
    half_w, half_h = int(w/2), int(h/2)

    # high pass filter
    n = 25
    dft_shift[half_w-n:half_w+n+1,half_h-n:half_h+n+1] = 0
    dft = np.asarray(dft_shift, dtype=np.uint8)
    mag = np.abs(dft_shift)
    A_mag = np.log10(1+abs(mag))
    rescaled1 = 255 * (A_mag - A_mag.min()) / A_mag.ptp()
    foto1 = Image.fromarray(rescaled1.astype(np.uint8), mode='L')
    foto1 = np.asarray(foto1, dtype=np.uint8)
    
    ang = np.angle(dft_shift)
    combined = np.multiply(mag, np.exp(1j*ang))
    fftx = np.fft.ifftshift(combined)
    ffty = np.fft.ifft2(fftx)
    imgCombined = np.abs(ffty)
    imgCombined = np.asarray(imgCombined, dtype=np.uint8)
    img_and_magnitude = np.concatenate((img, foto), axis=1)
    img_and_magnitude1 = np.concatenate((foto1, imgCombined), axis=0)
    cv2.imshow('Image and Fourier Transform', img_and_magnitude)
    cv2.imshow('Filtered Spectrum and Inverse Fourier Transform', img_and_magnitude1)
    cv2.waitKey(0)
   
   
    
    
    
    
my_btn3 = Button(root,  text="High Pass Filtering",  command=open3).pack(pady = 20, padx = 20)  


def open4(): 
    from PIL import Image, ImageDraw
    global  my_image2
    openV=Toplevel(root)
    #define the vertical filter
    root.filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("image files", 
                                                        "*.jpg*"), 
                                                       ("all files", 
                                                      "*.*")))
    img = cv2.imread(root.filename, cv2.IMREAD_GRAYSCALE)
    dft = np.array(img)
    dft = np.fft.fft2(dft)
    dft_shift = np.fft.fftshift(dft)
    #fft_x = np.abs(dft_shift)
    fft_x = np.log10(1+abs(dft_shift))
    rescaled = 255 * (fft_x - fft_x.min()) / fft_x.ptp()
    foto = Image.fromarray(rescaled.astype(np.uint8), mode='L')
    foto = np.asarray(foto, dtype=np.uint8)
    #cv2.imshow('Image and Fourier Transform', foto)
    
    
    x,y = dft_shift.shape[0],dft_shift.shape[1]
    #size of circle
    e_x,e_y=70,70
    #create a box 
    bbox=((x/2)-(e_x/2),(y/2)-(e_y/2),(x/2)+(e_x/2),(y/2)+(e_y/2))

    low_pass=Image.new("L",(dft_shift.shape[0],dft_shift.shape[1]),color=0)

    draw1=ImageDraw.Draw(low_pass)
    draw1.ellipse(bbox, fill=1)

    #low_pass_np=np.array(low_pass)
    #multiply both the images
    filtered=np.multiply(dft_shift,np.transpose(low_pass))
     

    mag = np.abs(filtered)
    A_mag = np.log10(1+abs(mag))
    rescaled1 = 255 * (A_mag - A_mag.min()) / A_mag.ptp()
    foto1 = Image.fromarray(rescaled1.astype(np.uint8), mode='L')
    foto1 = np.asarray(foto1, dtype=np.uint8) 
    
    ang = np.angle(filtered)
    combined = np.multiply(mag, np.exp(1j*ang))
    fftx = np.fft.ifftshift(combined)
    ffty = np.fft.ifft2(fftx)
    #imgCombined = np.abs(ffty)
    imgCombined = np.asarray(ffty, dtype=np.uint8)
    mag= np.asarray(mag, dtype=np.uint8)
    img_and_magnitude = np.concatenate((img, foto), axis=1)
    img_and_magnitude1 = np.concatenate((foto1, imgCombined), axis=0)
    cv2.imshow('Image and Fourier Transform', img_and_magnitude)
    cv2.imshow('Filtered Spectrum and Inverse Fourier Transform', img_and_magnitude1)
    cv2.waitKey(0)
         
my_btn4 = Button(root,  text="Low Pass Filtering",  command=open4).pack(pady = 20, padx = 20)  
root.mainloop()
                                           




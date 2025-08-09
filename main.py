import cv2
import numpy

import os
#Ensure that working directory= invoking directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys

import VectoriseStep
import DrawStep
import WriteStep

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()



print("please select starting image file.")
path = filedialog.askopenfilename()
#path=input("enter file name (with extension):\n\t")

if path[len(path)-3:len(path)]=="cva":
    
    print("You have selected a CVA file.")
    print("loading image...")
    colours,contours,shape=WriteStep.read(path)

    
else:
    colours,contours,shape=VectoriseStep.vectorise(path,1)
    #colours1,contours1,shape1=VectoriseStep.vectorise(path,1.5)
    #colours2,contours2,shape2=VectoriseStep.vectorise(path,2.0)

#print("CONTOUR TYPE!  ",type(contours[0]),type(contours[0][0]),type(contours[0][0][0]))
#print("CONTOUR EG!    ",(contours[0]))
#print("CONTOUR LEN!   ",len(contours[0]))
#print("COLOUR EG!     ",colours[0])
#print("COLOUR LEN  !",len(colours))
#print("COLOUR SCALAR TYPE!",type(colours[0]))
#print("COLOUR TYPE!   ",type(colours[0][0]))


#DrawStep.show(colours,contours,shape)

print(f"Finished with {len(contours)} contours")



#COMPARE!
doComparison=True

if doComparison:
    ogImg=cv2.imread(path,cv2.IMREAD_COLOR)

    #Multiplier=500/ogImg.shape[1]
    #Multiplier=380/ogImg.shape[1]
    #Multiplier=1.2
    #if ogImg.shape[1]<400:
    #    Multiplier=1.5
    for Multiplier in [1]: #[1.2]: # [1.2,1.5,2.0]:
        if Multiplier==1:#1.2:
            DrawStep.show(colours,contours,shape)
        #elif Multiplier==1.5:
        #    DrawStep.show(colours1,contours1,shape1)
        #else:
        #    DrawStep.show(colours2,contours2,shape2)
        if path[len(path)-3:len(path)]=="cva":
            quit()
        image=cv2.resize(ogImg,(int(Multiplier*ogImg.shape[1]),int(Multiplier*ogImg.shape[0])),interpolation=cv2.INTER_CUBIC)
        cv2.imshow(f"difference {Multiplier}",128+(image-DrawStep.out))
        diffImg=128+(image-DrawStep.out)
        print("MINIMUM",diffImg.min())
        print("MAXIMUM",diffImg.max())
        #threshdiff=cv2.threshold(src=image-DrawStep.out,maxval=255,thresh=150,type=cv2.THRESH_BINARY_INV)
        #cv2.imshow("difference Thresholded",threshdiff)
        cv2.waitKey(0)

#WRITE!

doWrite:bool=(input("Write to file (y/n)")=="y")
if doWrite:
    WriteStep.write(colours,contours,shape)
    #WriteStep.write(colours1,contours1,shape1)
    #WriteStep.write(colours2,contours2,shape2)
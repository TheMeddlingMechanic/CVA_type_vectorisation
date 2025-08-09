import cv2
import numpy

import os

import sys

import time


#Ensure that working directory= invoking directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


ImgPath="targetReal.webp"
ogImg=cv2.imread(ImgPath,cv2.IMREAD_COLOR)
Img=cv2.resize(ogImg,(300,250))
GreyScale = cv2.cvtColor(Img,cv2.COLOR_BGR2GRAY)
imgCh=numpy.array(Img)

#show image for testing purposes
cv2.imshow("image",Img)
cv2.waitKey(0)


imgCh=GreyScale
cv2.imshow("1channel",imgCh)
cv2.waitKey(0)




def get_cont_key(contour):
    return 50/cv2.contourArea(contour)

def do_thresh(threshdiff:int):
    contours=[]
    thresh = numpy.zeros(GreyScale.shape,numpy.uint8)
    thresh2=thresh.copy()
    VectImg = numpy.zeros_like(Img)
    for i in range(0,256,2):
        cv2.threshold(src=imgCh,dst=thresh,maxval=255,thresh=i+threshdiff,type=cv2.THRESH_BINARY_INV)
        cv2.imshow("thresh",thresh)
        #cv2.waitKey(0)
        cv2.threshold(src=imgCh,dst=thresh2,maxval=255,thresh=i,type=cv2.THRESH_BINARY_INV)
        cv2.imshow("thresh2",thresh2)
        #cv2.waitKey(0)
        thresh=thresh-thresh2
        cv2.imshow("thresh",thresh)
        #cv2.waitKey(0)


        cnt, _ =cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(cnt)>0:
            #contours.extend(cnt)
            for contour in cnt:
                if len(contour) > 2 and (cv2.contourArea(contour)>10):
            
                    contours.append(contour)
                    

            #contours.extend(cnt)
            print(len(contours))

        VectImg = numpy.zeros_like(Img)
        cv2.drawContours(VectImg, cnt, -1, (255, 255, 255), 1)
        cv2.imshow("vector",VectImg)
        #cv2.waitKey(0)
    contours.sort(key=get_cont_key)
    return contours


#contours, _ = cv2.findContours(imgCh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
VectImg = numpy.zeros_like(Img)



contoursTrue=do_thresh(40)

cv2.drawContours(VectImg, contoursTrue, -1, (255, 255, 255), 1)
cv2.imshow("vector",VectImg)
cv2.waitKey(0)

mask = numpy.zeros(GreyScale.shape,numpy.uint8)#creates an empy mask to fill contours
out  = numpy.zeros(Img.shape,numpy.uint8)#output stores average colour from each contour



def fillCont(contour:list):
    mask[...]=0 #Resets the mask every loop
    #cv2.fillConvexPoly(img=mask,points=contour[0],color=(255,255,255))
    cv2.drawContours(mask,contour,-1,255,thickness=cv2.FILLED)#Fills mask with white within borders for contour i
    cv2.imshow("mask",mask)#show mask for debugging
    #kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,1))
    #mask2=cv2.morphologyEx(mask, cv2.MORPH_ERODE ,kernel)
    cv2.drawContours(out,contour,-1,cv2.mean(Img,mask),thickness=cv2.FILLED)
    #cv2.fillPoly(img=out,pts=contour,color=cv2.mean(Img,mask))
    print(cv2.mean(Img,mask))
    cv2.imshow("out",out)
    ####cv2.waitKey(0)
    print(i)
    pass

#for i in range(len(contoursFalse)):
#    fillCont([contoursFalse[i]])

for i in range(len(contoursTrue)):
    fillCont([contoursTrue[i]])
cv2.imshow("out",out)




print(f"-------------------\nFinal size check:\n  OG IMAGE: {sys.getsizeof(Img)}\n  NEW VECTOR IMG: {sys.getsizeof(contoursTrue)}")#+sys.getsizeof(contoursFalse)}")

#for i in range(len(contours)):
#    mask[...]=0 #Resets the mask every loop
#    cv2.fillPoly(img=mask,pts=[contours[i]],color=(255,255,255))
#    #cv2.drawContours(mask,contours,i,(255,255,255),thickness=cv2.FILLED)#Fills mask with white within borders for contour i
#    cv2.imshow("mask",mask)#show mask for debugging
#    cv2.fillPoly(img=out,pts=[contours[i]],color=cv2.mean(Img,mask))
#    cv2.imshow("out",out)
#    cv2.waitKey(0)
#    print(i)
#print(len(contours))
##cv2.imshow("out",out)
#cv2.drawContours(VectImg, contours, -1, (255, 255, 255), 1)
cv2.imshow("vector",VectImg)

cv2.waitKey(0)
time.sleep(3)
cv2.waitKey(0)
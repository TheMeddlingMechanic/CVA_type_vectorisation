import cv2
import numpy

import os

import sys




def show(colours,contours,shape):#,myOut=numpy.array([])):
    #shape=(int(shape[0]*1.429),int(shape[1]*1.429))###

    global out

    #if myOut.all()==numpy.array([]).all():
    if True:
        out = numpy.zeros(shape,numpy.uint8)#output image
        print(shape)
        if len(shape)==3:
            if shape[2]!=3:
                shape[2]=3
        else:out = cv2.cvtColor(out,cv2.COLOR_GRAY2BGR)
    #else:
    #    print("TEST1")
    #    out=myOut

    cv2.imshow("myOUt",out)

    for i in range(len(contours)):
        #print("COLOUR DTYPE:  ",type(colours[i]))
        contour=contours[i]
        for point in contour:
            #point[0][0]=point[0][0]*1.429###
            #point[0][1]=point[0][1]*1.429###
            pass

        cv2.drawContours(out,[contour],-1,colours[i],thickness=cv2.FILLED)
    out = cv2.GaussianBlur(out, (7,7), 0)#FILLS HOLES IN CONTOURS
    for i in range(len(contours)):
        #print("COLOUR DTYPE:  ",type(colours[i]))
        contour=contours[i]
        for point in contour:
            #point[0][0]=point[0][0]*1.429###
            #point[0][1]=point[0][1]*1.429###
            pass

        cv2.drawContours(out,[contour],-1,colours[i],thickness=cv2.FILLED)
    cv2.imshow("out",out)

    cv2.waitKey(0)

#def fillCont(contour:list,colour):
#    cv2.drawContours(out,contour,-1,colour,thickness=cv2.FILLED)
#    pass
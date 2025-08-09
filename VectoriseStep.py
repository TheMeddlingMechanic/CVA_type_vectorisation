import cv2
import numpy

import os

import sys

import math

import random

#Ensure that working directory= invoking directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

reachedArea=False

def getAngle(a,b,c):
    #a = np.array([6,0])
    #b = np.array([0,0])
    #c = np.array([0,6])

    ba = a - b
    bc = c - b

    cosine_angle = numpy.dot(ba, bc) / (numpy.linalg.norm(ba) * numpy.linalg.norm(bc))
    angle = numpy.arccos(cosine_angle)

    return numpy.degrees(angle)

def getAngle2(a,b,c):
    #"""Counterclockwise angle in degrees by turning from a to c around b
    #    Returns a float between 0.0 and 360.0"""
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang
    


def getColours(contour:list,index):
    global reachedArea
    

    mask = numpy.zeros(GreyScale.shape,numpy.uint8)#creates an empy mask to fill contours

    mask[...]=0 #Resets the mask every loop
    #rmask = numpy.zeros(GreyScale.shape,numpy.uint8)#creates an empy mask to fill contours
    #rmask[...]=0
    #cv2.fillConvexPoly(img=mask,points=contour[0],color=(255,255,255))
    cv2.drawContours(mask,contour,-1,255,thickness=cv2.FILLED)#Fills mask with white within borders for contour i
    #cv2.imshow("mask",mask)#show mask for debugging
    
    useHierc=False

    useHierc2=True

    #if not reachedArea:
    #    if cv2.contourArea(numpy.array(contour))<15:
    #        useHierc2=False
    #    else:
    #        reachedArea=True
    #        useHierc2=True
    
    global contoursTrue
    #if random.randint(10)==1:
    
    print(100*(index/len(contoursTrue)),"%")

    if useHierc:
        for i in range(len(overlaps)):
            if index<overlaps[i]:
                rmask = numpy.zeros(GreyScale.shape,numpy.uint8)
                cv2.drawContours(rmask,[contoursTrue[overlaps[i]]],-1,255,thickness=cv2.FILLED)
                cv2.imshow("rmask",rmask)
                #cv2.waitKey(0)
                mask=cv2.subtract(mask,rmask)#truecontours[index])
    elif useHierc2:
        for i in range(len(insides)):
            if index==outsideis[i] and cv2.contourArea(contoursTrue[index])>80:
                rmask = numpy.zeros(GreyScale.shape,numpy.uint8)
                cv2.drawContours(rmask,[insides[i]],-1,255,thickness=cv2.FILLED)
                cv2.imshow("rmask",rmask)
                #cv2.waitKey(0)
                mask=cv2.subtract(mask,rmask)#truecontours[index])

    cv2.imshow("mask",mask)#show mask for debugging
    #cv2.waitKey(0)


    colors.append(cv2.mean(Img,mask))

def get_cont_key(contour):#Allows us to sort the contours ontop of eachother later

    if cv2.contourArea(contour)!=0:
        return 5000/cv2.contourArea(contour)
    else: return 50000000


def find_cnts(): ##UNUSED
    global imgCh
    global Img

    VectImg = numpy.zeros_like(Img)


    cnts=[]
    cnts, _ = cv2.findContours(imgCh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(VectImg, cnts, -1, (255, 255, 255), 2)
    cv2.imshow("VECTOR!!!",VectImg)
    print("LENGTH lol:",len(cnts))
    return cnts



def do_thresh(threshdiff:int):#Finds contours for image.Low diff is better for abstract, high for real images.
    
    contours=[]

    thresh = numpy.zeros(GreyScale.shape,numpy.uint8)
    thresh2=thresh.copy()
    VectImg = numpy.zeros_like(Img)
    for i in range(0,256,threshdiff-8):
        cv2.threshold(src=imgCh,dst=thresh,maxval=255,thresh=i+threshdiff,type=cv2.THRESH_BINARY_INV)
        ######cv2.imshow("thresh",thresh)
        #cv2.waitKey(0)
        cv2.threshold(src=imgCh,dst=thresh2,maxval=255,thresh=i,type=cv2.THRESH_BINARY_INV)
        ####cv2.imshow("thresh2",thresh2)
        #cv2.waitKey(0)
        thresh=thresh-thresh2
        #####cv2.imshow("thresh",thresh)
        #cv2.waitKey(0)



        #cnt, _ =cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        cnt0, _ =cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        #cnt=[]
        #for cont0 in cnt0:
        #    if cv2.contourArea(cont0)>0:
        #        cnt.append(cont0)
        #if len(cnt)==0:
        #    continue
        
        pointfix1=False

        cnt=[]
        for cont in cnt0:
            if cv2.contourArea(cont)>1:
                cnt.append(cont)
                
        if len(cnt)==0:
            continue
        if not pointfix1:
            
            for cont in cnt:
                myCont=[]
                cont=cv2.approxPolyDP(cont,0.050,True)
                for ipoint in range(len(cont)):
                    myCont.append(cont[ipoint])
                    if ipoint==0 or ipoint>=len(cont)-1:
                        myCont.append(cont[ipoint])
                        continue

                    a=cont[ipoint-1][0]
                    print(a)
                    b=cont[ipoint][0]
                    c=cont[ipoint+1][0]
                    angle=getAngle2(a,b,c)
                    if not (angle> 170 and angle < 190):
                        myCont.append(cont[ipoint])
                cont=numpy.array(myCont)
                if len(cont)<=2:
                    continue
                contours.append(cont)
            #    print(f"myCont has length {len(cont)}")
            #print("cnt HAD lenth ",oldCntLength, "but now HAS length ",len(cnt))
                #print("contours",len(contours))
        #cnt=oldCnt
        #print(contours[0])
        if len(contours)==0:
            continue

        if pointfix1:
            contours=[]
            
            if len(cnt)>0:
                #contours.extend(cnt)
                for contour in cnt:


                    ApproxCont=[]
                    ApproxCont.append(contour[0])

                    pointsToSkip=0

                    if len(contour)>30:
                        for p in range(1,len(contour)-9,1):
                            if pointsToSkip>0:
                                pointsToSkip-=1
                                pass
                            else:
                                angleFar=0
                                a=numpy.array([contour[p-8][0][0],contour[p-8][0][1]])
                                b=numpy.array([contour[p][0][0],contour[p][0][1]])
                                c=numpy.array([contour[p+8][0][0],contour[p+8][0][1]])
                                angleFar=getAngle(a,b,c)

                                angleNear=0
                                a=numpy.array([contour[p-1][0][0],contour[p-1][0][1]])
                                b=numpy.array([contour[p][0][0],contour[p][0][1]])
                                c=numpy.array([contour[p+1][0][0],contour[p+1][0][1]])

                                angleNear=getAngle(a,b,c)

                                if abs(angleFar)<175 or angleNear<175:
                                    ApproxCont.append(contour[p])
                                elif angleFar <=10 and angleNear <=10:
                                    pointsToSkip=1
                        ApproxCont.append(contour[-1])
                        ApproxCont=numpy.array(ApproxCont)

                        print("LEN: ",len(contour))
                        print("APPROX LEN: ",len(ApproxCont))
                    else:
                        ApproxCont=contour

                    contours.append(ApproxCont)
                    
                    #ApproxCont=contour
                    #if len(contour) > 2 and (cv2.contourArea(contour)>10):


                        #cv2.approxPolyDP(contour,5.0,True,ApproxCont)
                        #contours.append(ApproxCont)


                #contours.extend(cnt)
                print(len(contours))

            print(len(contours))
            VectImg = numpy.zeros_like(Img)
            cv2.drawContours(VectImg, cnt, -1, (255, 255, 255), 1)
            ######cv2.imshow("vector",VectImg)
            #cv2.waitKey(0)
    contours.sort(key=get_cont_key)
    

    contoursFinal=[]
    ###Remove overlapping contours
    pointfix2=False
    if pointfix2:
        for c1 in range(len(contours)-1,-1,-1):
            banC1=False
            #print("NewC1",c1,"/",len(contours))
            mask1= numpy.zeros(GreyScale.shape,numpy.uint8)
            cv2.drawContours(mask1,[contours[c1]],-1,255,thickness=cv2.FILLED)
            for c2 in range(c1):
                banC1=False
                mask2= numpy.zeros(GreyScale.shape,numpy.uint8)
                cv2.drawContours(mask2,[contours[c2]],-1,255,thickness=cv2.FILLED)

                overlap=mask1*mask2
                cOver,_=cv2.findContours(overlap,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                overlapArea=0
                #print(len(cOver))
                for overCont in cOver:
                    #print(type(overCont[0]))
                    overlapArea=overlapArea+cv2.contourArea(overCont)
                if overlapArea>=20:
                    if overlapArea > cv2.contourArea(contours[c2])*0.85 and overlapArea>cv2.contourArea(contours[c1])*0.9:
                        banC1=True
                        print("DELETED!!!")
                        break
            #print("lol")
            if not banC1:
                contoursFinal.append(contours[c1])
    else:
        for contour in contours:
            contoursFinal.append(contour)
            #contoursFinal=contours
            #print("contoursFin",len(contoursFinal))
    #for i in range(3):
    #    contoursFinal=approx_points_from_angles(contoursFinal)
    #contoursFinal=approx_points_from_angles(contoursFinal)
    ###global contoursTrue
    ###contoursTrue=contoursFinal
    ###contoursFinal=removeOverlapContours(contoursFinal)
    contoursFinal.sort(key=get_cont_key)
    #contoursFinal=contours

    return contoursFinal


def get_overlaps(trueConts):
    combination=numpy.zeros_like(imgCh)
    intersect=combination
    mask=combination

    global overlaps
    global overlapis
    overlaps=[]
    overlapis=[]

    for icontour in range(len(trueConts)):
        intersect[...]=0
        cv2.imshow("overlap",intersect)
        #cv2.waitKey(0)

        mask[...]=0
        cv2.drawContours(mask,[trueConts[icontour]],-1,255,thickness=cv2.FILLED)
        cv2.imshow("mask",mask)
        cv2.imshow("img1",combination)
        intersect=cv2.bitwise_and(mask,combination)
        cv2.imshow("overlap",intersect)
        #cv2.waitKey(0)
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        intersect=cv2.morphologyEx(intersect, cv2.MORPH_ERODE ,kernel)
        if not cv2.countNonZero(intersect)==0:
            overlaps.append(icontour)
            overlapis.append(mask)
        
        combination=cv2.add(mask,combination)
    #cv2.waitKey(0)
    print(len(overlaps))
    print(len(overlapis))

def get_bounds(contour):
    x_min, y_min, w, h = cv2.boundingRect(contour)
    x_max=x_min+w
    y_max=y_min+h

    return x_min,x_max,y_min,y_max

def get_sort_key_xmin(index):#Allows us to sort the contours by minimum x position
    x,y,w,h=get_bounds(contoursTrue[index])
    return x

def removeOverlapContours(trueConts:list):
    
    #newConts=trueConts
    newConts=[]
    toDelete=[]
    oldLen=len(trueConts)
    xSortedConts=[]
    for x in range(len(trueConts)):
        xSortedConts.append(x)
    #print(xSortedConts)
    xSortedConts.sort(key=get_sort_key_xmin)

    leng=len(xSortedConts)
    #tree=[]# tree is a list of dictionaries. Each has a "name" (str) and "children" (list of dictionaries)
    for i in range(len(xSortedConts)):
        print("i =",i,"/",leng)
        #is_child=2 #set to 2 by default. if found that it is a brach, set to one, if if found that it isn't, set to 0

        contour=trueConts[xSortedConts[i]]
        x_min,x_max,y_min,y_max=get_bounds(contour)
        for j in range(i+1,len(xSortedConts)):
            if j<=i:
                continue
            cont1=trueConts[xSortedConts[j]]
            x_min1,x_max1,y_min1,y_max1=get_bounds(cont1)
            if x_max1<x_max and y_max1<y_max and y_min1>y_min:
                if cv2.contourArea(trueConts[xSortedConts[j]])>=0.999*cv2.contourArea(trueConts[xSortedConts[i]]):
                    print("SHOULD DELETE")
                    toDelete.append(xSortedConts[j])
    for i in range(len(trueConts)):
        if not i in toDelete:
            newConts.append(trueConts[i])
    print(f"OLDLEN: {oldLen}, NEWLEN: {len(newConts)}")
    return newConts

def get_box_overlaps2(trueConts):

    global insides
    global insideis
    global outsides
    global outsideis
    insides=[]
    insideis=[]
    outsides=[]
    outsideis=[]

    
    #global xSortedConts
    xSortedConts=[]
    for x in range(len(trueConts)):
        xSortedConts.append(x)
    #print(xSortedConts)
    xSortedConts.sort(key=get_sort_key_xmin)

    leng=len(xSortedConts)
    #tree=[]# tree is a list of dictionaries. Each has a "name" (str) and "children" (list of dictionaries)
    for i in range(len(xSortedConts)):
        print("i =",i,"/",leng)
        #is_child=2 #set to 2 by default. if found that it is a brach, set to one, if if found that it isn't, set to 0

        contour=trueConts[xSortedConts[i]]
        x_min,x_max,y_min,y_max=get_bounds(contour)
        for j in range(i+1,len(xSortedConts)):
            if j<=i:
                continue
            cont1=trueConts[xSortedConts[j]]
            x_min1,x_max1,y_min1,y_max1=get_bounds(cont1)
            if x_max1<x_max and y_max1<y_max and y_min1>y_min:
                insideis.append(xSortedConts[j])
                outsideis.append(xSortedConts[i])
                insides.append(trueConts[xSortedConts[j]])
                outsides.append(trueConts[xSortedConts[i]])

def get_box_overlaps(trueConts):
    #global xSortedConts
    xSortedConts=list[range(len(trueConts))]
    xSortedConts.sort(key=get_sort_key_xmin)
    for i in range(len(xSortedConts)):
        contour=trueConts[xSortedConts[i]]
        x_min,x_max,y_min,y_max=get_bounds(contour)
        for j in range(len(xSortedConts)):
            if j<=i:
                continue
            cont1=trueConts[xSortedConts[j]]
            x_min1,x_max1,y_min1,y_max1=get_bounds(cont1)
            if x_max1<x_max and y_max1<y_max and y_min1>y_min:
                pass#is_child=search_tree(tree,xSortedConts[i],x_min,x_max,y_min,y_max,True)


def search_tree(searchList:list,icontour,x_min,x_max,y_min,y_max,insert:bool):
    for node in searchList:
        x_min2,x_max2,y_min2,y_max2=get_bounds(contoursTrue[node["name"]])
        #since each root is already in the tree, x_min2 must be lower than x_min
        if x_max<x_max2 and y_max<y_max2 and y_min>y_min2 and not node["name"]==icontour:
            if search_tree(node["children"],icontour,x_min,x_max,y_min,y_max,insert): #go iteratively until we find exactly where it is in the tree
                return True
            elif insert:
                node["children"].extend([{"name":icontour}])
                return True
            else:
                return False
        else:
            return False

def vectorise(path="",Multiplier=1,use_img=False,img=numpy.zeros(1,)):
    ImgPath=path
    ogImg=img
    if not use_img:
        ogImg=cv2.imread(ImgPath,cv2.IMREAD_COLOR)

    global Img

    #Multiplier=380/ogImg.shape[1]
    #Multiplier=500/ogImg.shape[1]
    #Multiplier=1.2 #=0.9
    #if ogImg.shape[1]<400:
    #    Multiplier=1.5 #=1.2

    #Multiplier=2.0
    print("Getting Image!")

    Img=cv2.resize(ogImg,(int(Multiplier*ogImg.shape[1]),int(Multiplier*ogImg.shape[0])),interpolation=cv2.INTER_CUBIC)
    #Img =(Img // 6) * 6 ##Quantise image
    global GreyScale
    GreyScale = cv2.cvtColor(Img,cv2.COLOR_BGR2GRAY)
    global imgCh
    imgCh=numpy.array(Img)

    #show image for testing purposes
    cv2.imshow("image",Img)
    #cv2.imshow("image",cv2.resize(ogImg,(int(Multiplier*ogImg.shape[1]),int(Multiplier*ogImg.shape[0]))))
    
    #cv2.imshow("image",cv2.resize(ogImg,(int(Multiplier*2*ogImg.shape[1]),int(Multiplier*2*ogImg.shape[0]))))
    print("Press ENTER to continue.")
    cv2.waitKey(0)

    imgCh=GreyScale

    #hsv_img = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)
    #imgCh=cv2.extractChannel(hsv_img,2)
    #GreyScale=imgCh

    cv2.imshow("1channel",imgCh)
    print("Press ENTER to continue.")
    cv2.waitKey(0)

    VectImg = numpy.zeros_like(Img)
    global contoursTrue

    print("starting thresh to get contours")
    contoursTrue=do_thresh(30)

    print("done getting contours!")
    #contoursTrue=find_cnts()

    print("drawing representation")
    cv2.drawContours(VectImg, contoursTrue, -1, (255, 255, 255), 1)
    cv2.imshow("vector",VectImg)
    print("Press ENTER to continue.")
    cv2.waitKey(0)

    global colors
    colors=[]
    
    print("getting overlapping contours")
    #get_overlaps(contoursTrue)
    get_box_overlaps2(contoursTrue)

    print("getting colours")

    for i in range(len(contoursTrue)):
        getColours([contoursTrue[i]],i)

    return colors, contoursTrue, Img.shape
import numpy

import json
import cv2

import os
#Ensure that working directory= invoking directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def write(colours:list,contours:list,shape):
    print(type(shape))
    name=""
    name=input("enter a filename to write to (no extension):\n\t")
    file=open(f"{name}.cva","wb")
    bigArr:list=[numpy.uint8(shape[0]//8)]
    bigArr.append(numpy.uint8(shape[1]//8))
    for i in range(len(contours)):
        bigArr.append(numpy.uint16(len(contours[i])))
        bigArr.append(numpy.uint8(colours[i][0]))
        bigArr.append(numpy.uint8(colours[i][1]))
        bigArr.append(numpy.uint8(colours[i][2]))
        #bigArr.extend(colours[i][:3])
        for x in range(len(contours[i])):
            for y in range(len(contours[i][x])):
                bigArr.append(numpy.uint16(contours[i][x][y][0]))
                bigArr.append(numpy.uint16(contours[i][x][y][1]))
    #print(bigArr[:800])
    #file.write(str(bigArr))
    #numpy.save(file,numpy.array(bigArr),False,False)
    numpy.savez_compressed(file,a=numpy.array(bigArr))
    file.close()



def read(path:str):
    #file=open(path,"wb")
    #bigArrStr=file.read()
    bigArrNump=numpy.load(path)
    #bigArr=bigArrNump.tolist()
    bigArr=bigArrNump['a'].tolist()

    #bigArrStr = json.loads(bigArrStr)
    #bigArr=[int(s) for s in bigArrStr]


    #shape=(int(bigArr[0])*8,500)
    shape=(int(bigArr[0])*8,int(bigArr[1])*8)
    
    colours=[]
    contours=[]

    current_contour_len=0
    on_step=0

    i=2
    while i < len(bigArr):
        if on_step==0:#find new contour length
            current_contour_len=bigArr[i]
            #print(current_contour_len)
            on_step=1
            i+=1

            #input(f"STEP: 1, position:{i} ,contourLen:{current_contour_len}-")
        elif on_step==1:
            #colorArr=numpy.ndarray(3,)
            #colorArr[0],colorArr[1],colorArr[2]=numpy.int8(bigArr[i]),numpy.int8(bigArr[i+1]),numpy.int8(bigArr[i+2])

            colour=(bigArr[i],bigArr[i+1],bigArr[i+2])

            colours.append(colour)
            on_step=2
            i+=3
            #input(f"STEP: 2, position:{i} ,colour:{tuple(colour)}-")
        else:
            #contour=numpy.ndarray((current_contour_len,1,2))#,dtype=numpy.ndarray)
            contour=[]
            for x in range(current_contour_len):
                try:
                    point=[int(bigArr[i+2*x]),int(bigArr[i+2*x+1])]
                    #point=[int(bigArr[i+2*x]),int(bigArr[i+2*x+1])]
                    contour.append([point])
                except IndexError:
                    pass
                    #print(len(bigArr))
                    #print("I",i)
            contours.append((numpy.array(contour)))
            on_step=0
            i+=current_contour_len*2
            #input(f"STEP: 3, position:{i} ,contourLen:{len(contour)}-")

    return colours,contours,shape
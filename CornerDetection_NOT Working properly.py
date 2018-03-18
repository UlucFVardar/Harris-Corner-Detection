import PIL.Image
from tkColorChooser import askcolor
import PIL.ImageTk
import numpy as np
import math
import data
import tkFileDialog

pix=None


def main():
    img=readImage() #gray image
    array = PIL2np(img) ## convert np.array
    gaus_filter = create_Gaussian_filter_x_y(sigma=1)
    img_Ix_Iy = make_it_gaussian_filtered(array, gaus_filter)
    img_Ixx_Ixy_Iyy = calculate_Ixx_Ixy_Iyy(img_Ix_Iy) 
    img_SIxx_SIxy_SIyy = calculate_SIxx_SIxy_SIyy(img_Ixx_Ixy_Iyy,11)
    img_R=responseOfDetector(img_SIxx_SIxy_SIyy)
    List=sortedRValues(img_R)	
    local_Max_list=findLocalMaximums(img_R,List,3)

    for i in range(0,len(local_Max_list)):
        if local_Max_list[i].list[0]>100000000:
            print int (local_Max_list[i].list[0]),
            x=local_Max_list[i].list[1]
            y=local_Max_list[i].list[2]
            print "x>",x," y>",y
            array[x][y]=0
    img_out=np2PIL(array)
    img_out.show()

    print "size",len(local_Max_list)

def responseOfDetector(trippleTupleMatrix):
    responseMatrix = [[0 for i in range(len(trippleTupleMatrix[0]))] for j in range(len(trippleTupleMatrix))]

    for i in range(len(trippleTupleMatrix)):
        for j in range((len(trippleTupleMatrix[0]))):
            if type(trippleTupleMatrix[i][j]) is tuple:
                SIxx, SIxy, SIyy = trippleTupleMatrix[i][j]
                d = data.Data()
                d.append(SIxx)
                d.append(SIxy)
                d.append(SIyy)
                RDataObject = data.Data()
                RDataObject.append(d.getR(0.2))  # data.list[0] = R
                RDataObject.append(i)  # data.list[1] = i
                RDataObject.append(j)  # data.list[2] = j
                responseMatrix[i][j] = RDataObject
            else:
                d = data.Data()
                d.append(0)
                d.dumi=True 
                responseMatrix[i][j] = d  # Rdataobjectler konuldu ama sinirlar 0 mi olacak?

    return responseMatrix


def sortedRValues(responseMatrix):
    length = len(responseMatrix) * len(responseMatrix[0])
    trashHoldList = []

    for i in range(len(responseMatrix)):
        for j in range(len(responseMatrix[0])):
            trashHoldList.append(responseMatrix[i][j])

    quickSort(trashHoldList)
    return trashHoldList


def findLocalMaximums(responseMatrix, trashHoldList, windowSize):
    startI = int(-windowSize / 2.)
    endI = int(windowSize / 2. + 1)
    localMaxList = []
    for i in range(len(trashHoldList) - 1, -1, -1):
        flag = 0    
        if trashHoldList[i].dumi==False:
            currentX = trashHoldList[i].list[1]
            currentY = trashHoldList[i].list[2]
            if responseMatrix[currentX][currentY].dumi==False:
                
                for j in range(startI, endI):    
                    for k in range(startI, endI):
                        if currentX-j >=0 and currentX-j <len(responseMatrix[0]) and currentY-k >=0 and currentY-k < len(responseMatrix):
                            if isinstance(responseMatrix[currentX-j][currentY-k],data.Data) and (j != 0 or k != 0):
                                responseMatrix[currentX - j][currentY - k].dumi=True
                              
        
    for i in range(len(responseMatrix)):
        for j in range(len(responseMatrix[0])):   
            if responseMatrix[i][j].dumi==False:
                localMaxList.append(responseMatrix[i][j])
               
    return localMaxList




def calculate_SIxx_SIxy_SIyy(img_Ixx_Ixy_Iyy,windowSize):
	(nrows, ncols) = len(img_Ixx_Ixy_Iyy),len(img_Ixx_Ixy_Iyy[0])    
	rangeS = int(windowSize -1 / 2)
	img_SIxx_SIxy_SIyy=[[ 0 for x in range (ncols)] for y in range(nrows)]
	for i in range(0, nrows):
		for j in range(0, ncols):
			if type(img_Ixx_Ixy_Iyy[i][j]) is tuple:
				sum_Ixx=0.
				sum_Ixy=0.
				sum_Iyy=0.
				for l in range(-rangeS, rangeS +1):
					for m in range (-rangeS, rangeS +1):
						if (i-l >= 0 and i-l < nrows) and (j-m >= 0 and j-m < ncols):
							if type(img_Ixx_Ixy_Iyy[i-l][j-m]) is tuple:
								xx,xy,yy=img_Ixx_Ixy_Iyy[i-l][j-m]
		                		sum_Ixx+=xx
		                		sum_Ixy+=xy
		                		sum_Iyy+=yy
				t=sum_Ixx,sum_Ixy,sum_Iyy
				img_SIxx_SIxy_SIyy[i][j]=t
	return img_SIxx_SIxy_SIyy
                	



def readImage():
	file_path_string = tkFileDialog.askopenfilename()
	fp =open (file_path_string)
	targetImage=PIL.Image.open(fp)
	#load command gives the pixel rgb values 

	img_gray = color2gray(targetImage)
	img_gray.show()
	global pix
	pix =img_gray.load()
	return img_gray

def PIL2np(img):
    nrows, ncols = img.size
    print("nrows, ncols:", nrows,ncols)
    imgarray = np.array(img)
    return  imgarray


def color2gray(img):
    img_gray = img.convert('L')
    return img_gray

def calculate_Ixx_Ixy_Iyy(img_Ix_Iy):
	ncols,nrows = len(img_Ix_Iy[0]),len(img_Ix_Iy)
	im_Ixx_Ixy_Iyy=[[ 0 for x in range (ncols)] for y in range(nrows)]
	for i in range(0, nrows):
		for j in range(0, ncols):
			if type(img_Ix_Iy[i][j]) is tuple:
				Ix,Iy= img_Ix_Iy[i][j]
				im_Ixx_Ixy_Iyy [i][j] = Ix*Ix, Ix*Iy, Iy*Iy
	return im_Ixx_Ixy_Iyy

def create_Gaussian_filter_x_y(sigma):
	
	interval=int(2*sigma+1)
	startI=int(-interval/2.)
	endI=int(interval/2.+1)
	filterG=[[0 for x in range(interval)]for y in range(interval)]
	for i in range(startI,endI):
		for j in range(startI,endI):
			source=math.exp( (i*i+j*j)/(2*sigma*sigma)*-1)
			filterG[i][j]=i*source*-1,j*source*-1
			print filterG[i][j],
		print ""
	return filterG

def make_it_gaussian_filtered(im, filter):
    (nrows, ncols) = im.shape
    (k1, k2) = len(filter[0]),len(filter)
    k1h = (k1 -1) / 2
    k2h = (k2 -1)/2
    im_out=[[ 0 for x in range (ncols)] for y in range(nrows)]
    for i in range(k1h, nrows-k1h):
        for j in range(k2h, ncols-k2h):
            sum_x = 0.
            sum_y = 0.
            for l in range(-k1h, k1h +1):
                for m in range (-k2h, k2h +1):
                	x,y= filter[l + k1h][m + k2h]
                	sum_x += im[i-l][j-m] * x
                	sum_y += im[i-l][j-m] * y
            im_out[i][j] = sum_x,sum_y
    return im_out





def np2PIL(im):
    print("size of arr:",im.shape)
    img = PIL.Image.fromarray(np.uint8(im))
    return img

def quickSort(alist):
    quickSortHelper(alist, 0, len(alist) - 1)


def quickSortHelper(alist, first, last):
    if first < last:
        splitpoint = partition(alist, first, last)

        quickSortHelper(alist, first, splitpoint - 1)
        quickSortHelper(alist, splitpoint + 1, last)


def partition(alist, first, last):
    pivotvalue = alist[first].list[0]

    leftmark = first + 1
    rightmark = last

    done = False
    while not done:

        while leftmark <= rightmark and alist[leftmark].list[0] <= pivotvalue:
            leftmark = leftmark + 1

        while alist[rightmark].list[0] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1

        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp

    temp = alist[rightmark]
    alist[rightmark] = alist[first]
    alist[first] = temp

    return rightmark





if __name__ == '__main__':
    main()
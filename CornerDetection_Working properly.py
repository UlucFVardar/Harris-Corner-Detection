import cv2
import numpy as np
import operator
import PIL.ImageTk
from Tkinter import *
import tkFileDialog
from PIL import ImageTk

root = Tk()


'''
This method is try to take the image 
@:parameter filename the filepath of the image
@:return img object taken form filepath
'''
def readImage(filename):
    img = cv2.imread(filename, 0)
    if img is None:
        print('Invalid image path :' + filename)
        return None
    else:
        print('Image successfully read...')
        return img

'''
This method is find the cornes of the image 
with using the harris corner detection algorithm method finds corners locations

to implement this method we used the convenience of some libraries like cv2, np, (np.gradient)...

'''
def findCorners(img, window_size, k, thresh):
    dy, dx = np.gradient(img)
    Ixx = dx ** 2
    Ixy = dy * dx
    Iyy = dy ** 2
    height = img.shape[0]
    width = img.shape[1]

    cornerList = []
    newImg = img.copy()
    color_img = cv2.cvtColor(newImg, cv2.COLOR_GRAY2RGB)
    offset = window_size / 2

    for y in range(offset, height - offset):
        for x in range(offset, width - offset):
            # Calculate sum of squares
            windowIxx = Ixx[y - offset:y + offset + 1, x - offset:x + offset + 1]
            windowIxy = Ixy[y - offset:y + offset + 1, x - offset:x + offset + 1]
            windowIyy = Iyy[y - offset:y + offset + 1, x - offset:x + offset + 1]
            Sxx = windowIxx.sum()
            Sxy = windowIxy.sum()
            Syy = windowIyy.sum()

            # Find determinant and trace, use to get corner response
            det = (Sxx * Syy) - (Sxy ** 2)
            trace = Sxx + Syy
            r = det - k * (trace ** 2)

            # If corner response is over threshold, color the point and add to corner list
            if r > thresh:
                #print (x, y, r)
                cornerList.append([x, y, r])
                color_img.itemset((y, x, 0), 100)  #b
                color_img.itemset((y, x, 1), 0)    #g
                color_img.itemset((y, x, 2), 255)  #r
    return color_img, cornerList

'''
This method opens a fileChooser and user can select a image from here
Method opens the image and add to screen it that detectConer method is called
@:parameter NO
@:return No
'''
def open_and_find_Corner():
    file_path_string = tkFileDialog.askopenfilename()
    fp = open(file_path_string, "rb")
    drawingImage = PIL.Image.open(fp)
    t = Label(root, text="Original Image")
    t.place(x=90, y=55)
    addToScreen(drawingImage, 50, 80)
    detectCorner(file_path_string)

'''
This method is set's the setUp values and if there is no proble with the image 
image converted grayImage
and Calls findCorners method 
then save image and also add to screen last view
'''
def detectCorner(path):
    img_path = path
    window_size = 5
    k = 0.04
    thresh = 10000000
    '''
    print ("information about setUp")
    print("Image Name: ", img_name)
    print("Window Size: ", str(window_size))
    print("K Corner Response: ", str(k))
    print("Corner Response Threshold:", int(thresh))    
    '''
    img = readImage(img_path)
    if img is not None:

        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        if len(img.shape) == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        '''
        print ("information about image properities")
        print ("Shape: " + str(img.shape))
        print ("Size: " + str(img.size))
        print ("Type: " + str(img.dtype))
        print ("The Original Image")
        print(img)
        '''
        finalImg, cornerList = findCorners(img, int(window_size), float(k), int(thresh))
        if finalImg is not None:
            cv2.imwrite("/Users/uluc/Desktop/finalimage.png", finalImg)
            fp = open("/Users/uluc/Desktop/finalimage.png", "rb")
            drawingImage = PIL.Image.open(fp)
            t = Label(root, text="The corners of the image have been found ")
            t.place(x=400,y=55)
            addToScreen(drawingImage, 440, 80)

'''
This method takes the image and resize it 
then print it to screen
@:parameter drawingImage image value
            xx the X coordinate of the image for add screen
            yy the Y coordinate of the image for add screen
'''
def addToScreen(drawingImage, xx, yy):
    drawingImage = drawingImage.resize((200, 200))
    render = ImageTk.PhotoImage(drawingImage)
    img = Label(root, image=render)
    img.image = render
    img.place(x=xx, y=yy)


'''
main method opens a interface and bind a button to screen 
'''
def main():
    global root
    root.title("Harris Corner Detection")
    root.geometry("700x300")
    pick_img = Button(root, text='Pick Image', command=open_and_find_Corner)
    pick_img.place(x=300, y=20)
    root.mainloop()


if __name__ == "__main__":
    main()
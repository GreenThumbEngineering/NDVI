from __future__ import division
import numpy
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cv2
from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb

"""CREATE FOLDERS CALLED COLORMAP AND CROP IN THE SAME FOLDER AS THIS PYTHON FILE"""

#loads colormap
colors = numpy.load('colors.npy', allow_pickle=True)

#loads original image
#this is used for colormapping
img = Image.open('testing.jpg').convert("RGB")

#loads original image without colormap
#this is used for segmentation
real_image = cv2.imread("testing.jpg")


"""
COLOR
MAPPING

"""
mask = numpy.asarray(img)

imgR, imgG, imgB = img.split()

arrG = numpy.asarray(imgG).astype('float')
arrR = numpy.asarray(imgR).astype('float')
arrB = numpy.asarray(imgB).astype('float')

redBlueDiff = (arrR  - arrB)
redBlueSum = (arrR + arrB)

redBlueSum[redBlueSum ==0] = 0.01

arrNDVI = redBlueDiff/redBlueSum
arrNDVI[arrNDVI == 0] = -1
sumAll = 0
amount = 0.00001

for row in arrNDVI:
    for pix in row:
         if pix != -1:
            sumAll += pix
            amount += 1

fastiecm=LinearSegmentedColormap.from_list('mylist', colors)

#saves colormapped original image
plt.imsave("./colormap/delete_later.jpg",arrNDVI,cmap=fastiecm, vmin=-1.0, vmax=1.0)



"""
IMAGE
SEGMENTATION

"""
#loads colormapped image
image = cv2.imread("./colormap/delete_later.jpg")

mask = numpy.zeros(image.shape[:2], numpy.uint8)
backgroundModel = numpy.zeros((1, 65), numpy.float64) 
foregroundModel = numpy.zeros((1, 65), numpy.float64) 

#CUSTOM VALUES HERE
#rectangle = (450,0,600,500)
#rectangle = (350,100,600,619)
#rectangle = (449,250,341,390)
#rectangle = (350,0,700,719)
#rectangle = (310,10,580,620)

#rectangle = (315,19,700,630)
rectangle = (0,0,1279,719)


#makes mask from colormapped image
cv2.grabCut(image, mask, rectangle,   
            backgroundModel, foregroundModel, 
            10, cv2.GC_INIT_WITH_RECT) 
mask2 = numpy.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')

#applies mask of the colormapped image to the original image
real_image = real_image * mask2[:, :, numpy.newaxis]

#saves the cropped image
cv2.imwrite('./crop/cropped.jpg', real_image)



"""
NDVI
CALCULATIONS

"""
#loads the cropped image
img = Image.open('./crop/cropped.jpg').convert("RGB")
mask = numpy.asarray(img)
imgR, imgG, imgB = img.split()

arrG = numpy.asarray(imgG).astype('float')
arrR = numpy.asarray(imgR).astype('float')
arrB = numpy.asarray(imgB).astype('float')

redBlueDiff = (arrR  - arrB)
redBlueSum = (arrR + arrB)

redBlueSum[redBlueSum ==0] = 0.01

arrNDVI = redBlueDiff/redBlueSum
arrNDVI[arrNDVI == 0] = -1
sumAll = 0
amount = 0.00001


for row in arrNDVI:
    for pix in row:
         if pix != -1:
            sumAll += pix
            amount += 1

print(sumAll/float(amount))

fastiecm=LinearSegmentedColormap.from_list('mylist', colors)

#saves the final NDVI calculated image
plt.imsave("./ndvi-calculated/%.4f.jpg" % (sumAll/float(amount)),arrNDVI,cmap=fastiecm, vmin=-1.0, vmax=1.0)


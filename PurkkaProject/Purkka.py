# INSTALL CV2 WITH pip install opencv-python
import cv2,os

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # iterate over all the entries
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        # if entry is a directory then get the list of files here 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles
def splitImage(image):
    #print(image)
    img = cv2.imread(image)
    height,width = img.shape[:2]
    # Splits image into 4 equal parts
    # For Arttu's data check the pixels yourself to find good lines
    #Vasen yla
    measurements = []

    crop_img1 = img[0:int(height/2), 0:int(width/2)]
    crop_img2 = img[0:int(height/2), int(width/2):width]
    crop_img3 = img[int(height/2):height, 0:int(width/2)]
    crop_img4 = img[int(height/2):height, int(width/2):width]

    measurements.append(crop_img1)
    measurements.append(crop_img2)
    measurements.append(crop_img2)
    measurements.append(crop_img4)
    path = (image.replace('png','jpg')).split('ndvi')
    x = '1'
    cv2.imwrite('/Users/samisirvio/PurkkaProject/ndvi_crop1/' + x + path[2], crop_img1)
    x = '2'
    cv2.imwrite('/Users/samisirvio/PurkkaProject/ndvi_crop2/' + x + path[2], crop_img2)
    x = '3'
    cv2.imwrite('/Users/samisirvio/PurkkaProject/ndvi_crop3/' + x + path[2], crop_img3)
    x = '4'
    cv2.imwrite('/Users/samisirvio/PurkkaProject/ndvi_crop4/' + x + path[2], crop_img1)

    return measurements



def splitTo4(allFiles):
    images = []
    for image in allFiles:
        images.append(splitImage(image))
    return images
#print(getListOfFiles('/Users/samisirvio/PurkkaProject/ndvi'))
def main():
    lista = getListOfFiles('/Users/samisirvio/PurkkaProject/ndvi')
    ret = splitTo4(lista)
    #print(ret)
main()
# Reads image from same folder as python file
# img = cv2.imread("plant2.jpg")
# height, width = img.shape[:2]
# ​
# # Splits image into 4 equal parts
# # For Arttu's data check the pixels yourself to find good lines
# #Vasen yla
# crop_img1 = img[0:height/2, 0:width/2]
# crop_img2 = img[0:height/2, width/2:width]
# ##Vasen ala 
# crop_img3 = img[height/2:height, 0:width/2]
# crop_img4 = img[height/2:height, width/2:width]
# ​
# ​
# cv2.imwrite('C:/Users/Elias/Desktop/Greenthumb_new/CROP/plant2_crop1.jpg', crop_img1)
# cv2.imwrite('C:/Users/Elias/Desktop/Greenthumb_new/CROP/plant2_crop2.jpg', crop_img2)
# cv2.imwrite('C:/Users/Elias/Desktop/Greenthumb_new/CROP/plant2_crop3.jpg', crop_img3)
# cv2.imwrite('C:/Users/Elias/Desktop/Greenthumb_new/CROP/plant2_crop4.jpg', crop_img4)



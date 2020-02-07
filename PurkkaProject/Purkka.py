# INSTALL CV2 WITH pip install opencv-python
import cv2,os
import pandas
from pathlib import Path

#Here you have your NDVI folder
data_folder = Path("C:/Users/Aleksi/NDVI/PurkkaProject/")

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
    #print(img.shape)   #600,800,3
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
    cv2.imwrite(str((data_folder / 'ndvi_crop1' / (x + path[2]) )), crop_img1)
    #print("Now printing here: " + str((data_folder / 'ndvi_crop1' / (x + path[2]) )))
    x = '2'
    cv2.imwrite(str((data_folder / 'ndvi_crop2' / (x + path[2]) )), crop_img2)
    x = '3'
    cv2.imwrite(str((data_folder / 'ndvi_crop3' / (x + path[2]) )), crop_img3)
    x = '4'
    cv2.imwrite(str((data_folder / 'ndvi_crop4' / (x + path[2]) )), crop_img4)

    return measurements



def splitTo4(allFiles):
    images = []
    for image in allFiles:
        images.append(splitImage(image))
    return images
#print(getListOfFiles('/Users/samisirvio/PurkkaProject/ndvi'))

#@author Leksuu
def imgNdvi():
    #open image into a matrix or smth
    imagesprocessedcount = 0
    print("päästii ndvi funktioon")
    for num in range(1,5): #1 to 4
        df = pandas.DataFrame(columns=['NDVI'])
        lista = getListOfFiles( data_folder / ('ndvi_crop' + str(num)) )
        rCoeff = 1
        gCoeff = 1
        bCoeff = 1
        for imgDir in lista:
            #print("11")
            ndvi = 0.0
            count = 0
            img = cv2.imread(imgDir)    #numpy.ndarray
            jj = 0
            for j in img:
                #print("22")
                jj+=1
                ii = 0
                for i in j:
                    ii +=1
                    #laske noist RGB:stä joku arvo välil -1,1
                    #1 = [0,255,0], -1 = [255,0,255],       G/255 - B/255 - R/255
                    R = int(i[0])
                    G = int(i[1])
                    B = int(i[2])
                    ndviAdd = ((gCoeff*G) + (bCoeff*B) - (rCoeff*R))/float(255)
                    ndvi += ndviAdd
                    #if jj % 50 == 0:
                        #print("RGB: " + str(i) + ", i: " + str(ii) + " ,j: " + str(jj))
                        #print("\npixel NDVI: " + str(ndviAdd))
                    count += 1
            ndvi = ndvi / float(count)
            print("Image's NDVI: " + str(ndvi))
            #print("df b4")
            #print(df)
            df = df.append({'NDVI': str(ndvi)}, ignore_index = True)  
            #print("df after")
            #print(df)
            imagesprocessedcount += 1
            print("imagesprocessedcount: " + str(imagesprocessedcount) + ", num: " + str(num))
        print("Dataframe for set " + str(num) + ":\n")
        print(df)
        df.to_csv('1+11csv' + str(num) + '.csv')
        print("Wrote df as a csv (hopefully)")
    #count = 0
    #for i in matrix:
    #    for j in i:
    #        ndvi += get-1+1valuefromRGB
    #        count += 1
    #ret ndvi / float(count) #hard div, not modulo
    return 1

def main():
    lista = getListOfFiles(data_folder / 'ndvi')
    #ret = 
    splitTo4(lista)
    #Now the splitting has been done. Time to count ndvis
    print("moi")
    imgNdvi()
    ret = 1
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



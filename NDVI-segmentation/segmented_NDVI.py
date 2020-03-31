from __future__ import division
import sys, traceback
from cv2 import imread, imwrite, split, cvtColor, COLOR_BGR2RGB
import numpy as np
import argparse
from plantcv import plantcv as pcv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb

def crop(img, pos):
    image = imread(img)
    height, width = image.shape[:2]
    middle = int(width/2)
    # Borders
    #left = 220
    #right = 200
    #top = 165
    #bot = 110
    left = 220
    right = 160
    top = 140
    bot = 60
    if pos == 1:
        crop_img = image[top:height-bot, left:middle]
    elif pos == 2:
        crop_img = image[top:height-bot, middle:width-right]
    else:
        crop_img = image[top:height-bot, left:width-right]
    
    return crop_img

def segmentation(imgW, imgNIR, shape):
    # VIS example from PlantCV with few modifications

    # Higher value = more strict selection
    s_threshold = 165
    b_threshold = 200

    # Read image
    img = imread(imgW)
    #img = cvtColor(img, COLOR_BGR2RGB)
    imgNIR = imread(imgNIR)
    #imgNIR = cvtColor(imgNIR, COLOR_BGR2RGB)
    #img, path, img_filename = pcv.readimage(filename=imgW, mode="native")
    #imgNIR, pathNIR, imgNIR_filename = pcv.readimage(filename=imgNIR, mode="native")

    # Convert RGB to HSV and extract the saturation channel
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')

    # Threshold the saturation image
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=s_threshold, max_value=255, object_type='light')

    # Median Blur
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

    # Convert RGB to LAB and extract the Blue channel
    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')

    # Threshold the blue image ORIGINAL 160
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=b_threshold, max_value=255, object_type='light')
    b_cnt = pcv.threshold.binary(gray_img=b, threshold=b_threshold, max_value=255, object_type='light')

    # Join the thresholded saturation and blue-yellow images
    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_cnt)

    # Apply Mask (for VIS images, mask_color=white)
    masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')

    # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

    # Threshold the green-magenta and blue images
    # 115
    # 135
    # 128
    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, max_value=255, object_type='light')
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')

    # Join the thresholded saturation and blue-yellow images (OR)
    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)

    # Fill small objects
    ab_fill = pcv.fill(bin_img=ab, size=200)

    # Apply mask (for VIS images, mask_color=white)
    masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')

    # Identify objects
    id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)

    # Define ROI
    height = shape[0]
    width = shape[1]
    roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=0, y=0, h=height, w=width)

    # Decide which objects to keep
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')

    # Object combine kept objects
    obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)
    
    # Filling holes in the mask, works great for alive plants, not so good for dead plants
    filled_mask = pcv.fill_holes(mask)

    final = pcv.apply_mask(img=imgNIR, mask=mask, mask_color='white')
    pcv.print_image(final, "./segment/segment-temp.png")

def NDVI(segmented):
    colors = np.load('colors.npy', allow_pickle=True)
    img = imread(segmented)
    mask = np.asarray(img)
    imgB, imgG, imgR = split(img)

    arrG = np.asarray(imgG).astype('float')
    arrR = np.asarray(imgR).astype('float')
    arrB = np.asarray(imgB).astype('float')

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

    plt.imsave("./ndvi-calculated/%.4f.jpg" % (sumAll/float(amount)),arrNDVI,cmap=fastiecm, vmin=-1.0, vmax=1.0)
    return sumAll/float(amount)


# Used for debugging, on server we run everything separately
def main(imgW, imgNIR, pos):
    #Crops both pics here
    pos = int(pos)
    croppedW  = crop(imgW, pos)
    imwrite('./crop/cropW-temp.png', croppedW)
    croppedNIR  = crop(imgNIR, pos)
    imwrite('./crop/cropNIR-temp.png', croppedNIR)
    #Segments image, gets mask from cropW, and applies it to cropNIR
    shape = croppedW.shape[:2]
    segmentation(imgW='./crop/cropW-temp.png', imgNIR='./crop/cropNIR-temp.png', shape=shape)
    #NDVI from segmented image
    NDVI('./segment/segment-temp.png')

if __name__== "__main__":
    parser = argparse.ArgumentParser(description="Give images and location")
    parser.add_argument("-w", "--imageW", help="Input white image file.", required=True)
    parser.add_argument("-n", "--imageNIR", help="Input NIR image file.", required=True)
    parser.add_argument("-p", "--position", help="1 or 2", required=True)
    args = parser.parse_args()
    main(imgW=args.imageW, imgNIR=args.imageNIR, pos=args.position)

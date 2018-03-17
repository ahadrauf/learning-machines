import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt 

#Adapted from this StackOverflow post: https://stackoverflow.com/questions/24385714/detect-text-region-in-image-using-opencv
def autocrop(image, width=1200, height=1000):
    img = image.copy()
    img = cv2.GaussianBlur(img, (5,5), 0)
    if img.shape[0] < img.shape[1]:
        img = imutils.resize(img, width=width)
    else:
        img = imutils.resize(img, height=height)

    img_final = image.copy()
    if img_final.shape[0] < img_final.shape[1]:
        img_final = imutils.resize(img_final, width=width)
    else:
        img_final = imutils.resize(img_final, height=height)
    img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_TRUNC)
    image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
    _, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
    
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation

    _, contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours
    
    focusArea = max(contours, key=lambda c: np.prod(cv2.boundingRect(c)[2:3]))
    [x, y, w, h] = cv2.boundingRect(focusArea)
    cropped = img_final[y:y+h, x:x+w]
    
    alteredCrop = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    filteredCrop = cv2.adaptiveThreshold(alteredCrop,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,13,6)
    filteredCrop = cv2.GaussianBlur(filteredCrop, (1, 1), 0)
    
    #Uncomment the lines below to visualize the images for debugging purposes
    '''
    if alteredCrop.shape[0] < alteredCrop.shape[1]:
        plot_image = np.concatenate((alteredCrop, filteredCrop), axis=0)
    else:
        plot_image = np.concatenate((alteredCrop, filteredCrop), axis=1)
    plt.imshow(plot_image, 'gray')
    plt.show()
    '''
    
    return (cropped, filteredCrop)
from pytesser import *
from PIL import Image
import os
import cv2
from matplotlib import pyplot as plt
import imutils

import sys
import textDetection
import formatText

def readText(image, contours):
    for contour in contours:
        [x, y, w, h] = contour
        temp_image = image[y:y+h, x:x+w]
        #temp_image = imutils.resize(temp_image, width=50)
        #print(temp_image.shape, x, y, w, h)
        cv2.imshow('temp', temp_image)
        cv2.waitKey()
        cv2.imwrite('temp_image.jpg', temp_image)
        print(image_to_string(Image.open('temp_image.jpg')).strip())
        sys.stdout.flush()
    os.remove('temp_image.jpg')
    
    
def contourBasedTextRecognition(image, contours, dilationIterations = 1):
    dates = []
    lots = []
    for contour in contours:
        [x, y, w, h] = contour[0]
        temp_image = image[int(y+h/2):y+h, int(x+w/2.4):x+w]
        #temp_image = image[y:y+h, x:x+w]
        #if len(contours) > 1:
        #    c = textDetection.detectText(temp_image.copy(), dilationIterations)
        cv2.imwrite('temp_image.jpg', temp_image)
        image_text = image_to_string(Image.open('temp_image.jpg')).strip()
        #if len(image_text) > 0:
        dates.append(image_text)
        
        temp_image = image[y:int(y+h/2), x:x+w]
        #temp_image = image[y:y+h, x:x+w]
        #if len(contours) > 1:
        #    c = textDetection.detectText(temp_image.copy(), dilationIterations)
        cv2.imwrite('temp_image.jpg', temp_image)
        image_text = image_to_string(Image.open('temp_image.jpg')).strip()
        #if len(image_text) > 0:
        lots.append(image_text)
        #cv2.imshow('temp', temp_image)
        #cv2.waitKey()
        #print(image_text)
        #sys.stdout.flush()
    os.remove('temp_image.jpg')
    return (dates, lots)
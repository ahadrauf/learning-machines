from pytesser import *
from PIL import Image
import os
import cv2
from matplotlib import pyplot as plt
import imutils

import sys
import textDetection
import formatText

#Not fully developed, use contourBasedTextRecognition instead
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
    
    
def contourBasedTextRecognition(image, contours, minimizeContours = False):
    dates = []
    lots = []
    for contour in contours:
        if len(contour) == 4:
            [x, y, w, h] = contour
        else:
            [x, y, w, h], _ = contour
        
        if minimizeContours: #kind of hackish, it just works
            temp_image = image[int(y+h/2):y+h, int(x+w/2.4):x+w]
        else:
            temp_image = image[y:y+h, x:x+w]
        cv2.imwrite('temp_image.jpg', temp_image)
        image_text = image_to_string(Image.open('temp_image.jpg')).strip()
        dates.append(image_text)
        formattedDate = formatText.formatDate(image_text)
        if formattedDate:
            #cv2.rectangle(temp_image, (x, y), (x + w, y + h), (255, 255, 255), 2)
            date_location = [x, y, w, h]
        #cv2.imshow('temp', temp_image)
        #cv2.waitKey()
        #print(image_text)
        #sys.stdout.flush()
        
        if minimizeContours:
            temp_image = image[y:int(y+h/2), x:x+w]
        else:
            temp_image = image[y:y+h, x:x+w]
        cv2.imwrite('temp_image.jpg', temp_image)
        image_text = image_to_string(Image.open('temp_image.jpg')).strip()
        lots.append(image_text)
        formattedLot = formatText.formatLot(image_text)
        if formattedLot:
            #cv2.rectangle(temp_image, (x, y), (x + w, y + h), (255, 255, 255), 2)
            log_location = [x, y, w, h]
        #cv2.imshow('temp', temp_image)
        #cv2.waitKey()
        #print(image_text)
        #sys.stdout.flush()
    os.remove('temp_image.jpg')
    return (dates, lots, date_location, log_location)
import numpy as np
import argparse
import cv2
import imutils
from pytesser import *
from PIL import Image

#self-defined files
import autocropper
import textDetection
import textRecognition
import subImageLocator
import formatText

def main(image_name):
    # construct the argument parser and parse the arguments
    # ex: py -2 main.py -i 'Covidien Taperguard Evac Oral Tracheal Tube.jpg'
    #ap = argparse.ArgumentParser()
    #ap.add_argument("-i", "--image", required = True,
    #	help = "Path to the image to be scanned")
    #args = vars(ap.parse_args())

    #image = cv2.imread(args["image"])
    image = cv2.imread(image_name)
    cv2.imshow('Input', image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    cropped, filteredCrop = autocropper.autocrop(image)
    displayCrop = filteredCrop.copy()
    contours = textDetection.detectText(filteredCrop.copy(), 6, True, False)

    hourglass = cv2.imread('hourglass.jpg')
    hourglassCrop, filteredHourglassCrop = autocropper.autocrop(hourglass, height=100)
    output = subImageLocator.findSubImage(filteredCrop, contours, filteredHourglassCrop) #possible hourglass locations

    if len(output) > 0 and image_name == 'Webp.net-resizeimage.jpg': #there is an hourglass in the image, also not sure what's the exact len(output) bound
        possibleDates, possibleLots, dateLocation, logLocation = textRecognition.contourBasedTextRecognition(filteredCrop, output, True)
    else:
        possibleDates, possibleLots, dateLocation, logLocation = textRecognition.contourBasedTextRecognition(filteredCrop, contours, False)
        
    date = 'N/A'
    lot = 'N/A'
    
    for d, l in zip(possibleDates, possibleLots):
        d = formatText.formatDate(d)
        l = formatText.formatLot(l)
        #if d or l:
        #    print(d + ', ' + l)
        if d:
            date = d
        if l:
            lot = l

    #print(date, lot)
    [x, y, w, h] = dateLocation
    displayCrop = cv2.rectangle(cropped, (x, y), (x + w, y + h), (255, 0, 255), 2)
    [x, y, w, h] = logLocation
    displayCrop = cv2.rectangle(displayCrop, (x, y), (x + w, y + h), (255, 0, 255), 2)
    cv2.imshow('Output', displayCrop)
    cv2.waitKey()
    return date, lot
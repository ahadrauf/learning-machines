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
 
# construct the argument parser and parse the arguments
# ex: py -2 main.py -i 'Covidien Taperguard Evac Oral Tracheal Tube.jpg'
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cropped, filteredCrop = autocropper.autocrop(image)
contours = textDetection.detectText(filteredCrop.copy(), 6, False)
#print(len(contours))
#contours = textDetection.detectText(filteredCrop.copy(), 5, True)
#print(len(contours))

#import sys
#sys.exit(0)
#textRecognition.readText(filteredCrop, contours)

hourglass = cv2.imread('hourglass.jpg')
hourglassCrop, filteredHourglassCrop = autocropper.autocrop(hourglass, height=100)
output = subImageLocator.findSubImage(filteredCrop, contours, filteredHourglassCrop)

possibleDates, possibleLots = textRecognition.contourBasedTextRecognition(filteredCrop, output)
for d, l in zip(possibleDates, possibleLots):
    d = formatText.formatDate(d)
    l = formatText.formatLot(l)
    #if d or l:
    #    print(d + ', ' + l)
    if d:
        date = d
    if l:
        lot = l

print(date, lot)
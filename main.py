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
import formatDate
 
# construct the argument parser and parse the arguments
# ex: py -2 main.py -i 'Covidien Taperguard Evac Oral Tracheal Tube.jpg'
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

cropped, filteredCrop = autocropper.autocrop(args["image"])
contours = textDetection.detectText(filteredCrop, 6)
#textRecognition.readText(filteredCrop, contours)

hourglassCrop, filteredHourglassCrop = autocropper.autocrop('hourglass.jpg', height=100)
output = subImageLocator.findSubImage(filteredCrop, contours, filteredHourglassCrop)

possibleDates = textRecognition.temp(filteredCrop, output)
for d in possibleDates:
    formattedDate = formatDate.formatDate(d)
    if formattedDate:
        print(formattedDate)
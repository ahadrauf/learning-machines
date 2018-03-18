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

def parseImage(image_name):	
    image = cv2.imread(image_name)
	#Display input image
    cv2.imshow('Input', image)
    cv2.waitKey()
    cv2.destroyAllWindows()
	
	#Autocrop the image around the field of active interest
	#cropped = just a cropped version of the original image
	#filteredCrop = the actual processed + cropped image (but in grayscale)
    cropped, filteredCrop = autocropper.autocrop(image)
	
	#Stores the contours of all the active sections of the cropped image
	#Note that 'active section' is just a fancy way of saying 'a place where something of note is located'
	#Note that the second parameter is right now hard-coded, TODO: should automate how that's selected
    contours = textDetection.detectText(filteredCrop.copy(), 6, True)

	#Locate all the possible matches for where an hourglass could be in the image
    hourglass = cv2.imread('tags/hourglass.jpg')
    hourglassCrop, filteredHourglassCrop = autocropper.autocrop(hourglass, height=100)
    output = subImageLocator.findSubImage(filteredCrop, contours, filteredHourglassCrop) #possible hourglass locations

	#If you found an hourglass, find the date using the hourglass as a reference
	#TODO: Right now I'm just using the image name as a check, but I think there should be a specific
	#		threshold for output that determines whether or not you can use it as a reference (it might not be length, though.
	#		Note that each entry in output is formatted as ([x, y, w, h], number_of_matches), so it might help to use the number_of_matches
	#		somehow)
    if len(output) > 0 and image_name == 'examples/Webp.net-resizeimage.jpg': #there is an hourglass in the image, also not sure what's the exact len(output) bound
        possibleDates, possibleLots, dateLocation, logLocation = textRecognition.contourBasedTextRecognition(filteredCrop, output, True)
    else: #If you can't use the hourglass as a reference, just look at all the contours
        possibleDates, possibleLots, dateLocation, logLocation = textRecognition.contourBasedTextRecognition(filteredCrop, contours, False)
        
	#Find the expiration date and lot number
    date = 'N/A'
    lot = 'N/A'    
    for d, l in zip(possibleDates, possibleLots):
        d = formatText.formatDate(d)
        l = formatText.formatLot(l)
        if d:
            date = d
        if l:
            lot = l
	
	#Display date and log on original image
    [x, y, w, h] = dateLocation
    displayCrop = cv2.rectangle(cropped, (x, y), (x + w, y + h), (255, 0, 255), 2)
    [x, y, w, h] = logLocation
    displayCrop = cv2.rectangle(displayCrop, (x, y), (x + w, y + h), (255, 0, 255), 2)
    cv2.imshow('Output', displayCrop)
    cv2.waitKey()
	
    return date, lot
	
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True,
    	help = "Path to the image to be scanned")
    args = vars(ap.parse_args())
	return parseImage(args["image"])
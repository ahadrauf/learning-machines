import numpy as np
import argparse
import cv2
import imutils

#self-defined files
import autocropper
import textDetection
 
# construct the argument parser and parse the arguments
# ex: py -2 main.py -i 'Covidien Taperguard Evac Oral Tracheal Tube.jpg'
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

cropped, filteredCrop = autocropper.autocrop(args["image"])
textDetection.detectText(filteredCrop)
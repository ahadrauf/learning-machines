import cv2
import imutils
from numpy import prod

def captch_ex(file_name, width=1200):
    img = cv2.imread(file_name)
    img = imutils.resize(img, width=width)

    img_final = cv2.imread(file_name)
    img_final = imutils.resize(img_final, width=width)
    img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
    ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
    
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation

    _, contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours
    
    contours = sorted(contours, key=lambda c: -prod(cv2.boundingRect(c)[2:3]))
    [x, y, w, h] = cv2.boundingRect(contours[0])
    cropped = img_final[y:y+h, x:x+w]
    cv2.imshow('captcha_result', cropped)
    cv2.waitKey()
	return cropped

file_name = 'Covidien Taperguard Evac Oral Tracheal Tube.jpg'
#file_name = 'Closurefast Introducer Sheath Set.jpg'
file_name = 'Lifeshield Male Femake Sterile Cap blurry.jpg'
file_name = 'Monocryl suture - Violet Monofilament.jpg'
file_name = 'BD Spinal Needle.jpg'
captch_ex(file_name)
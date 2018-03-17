import cv2
import numpy as np

def detectText(image):
    #2D filtering algorithm taken from: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
    #2D filtering blurs out noise while keeping important features (the features are also blurred, but they're still visible)
    kernel = np.ones((5,5),np.float32)/25
    processedImage = cv2.filter2D(image,-1,kernel)
    #cv2.imshow('temp', processedImage)
    #cv2.waitKey()
    if (len(image.shape) > 2):
        gray = cv2.cvtColor(processedImage,cv2.COLOR_BGR2GRAY) # grayscale
    else:
        gray = processedImage
    _, thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
    cv2.imshow('temp', thresh)
    cv2.waitKey()
    
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))    
    dilated = cv2.dilate(thresh,kernel,iterations = 6) # dilate (the number of iterations is experimental, change if needed)
    cv2.imshow('temp', dilated)
    cv2.waitKey()
    
    _, contours, _ = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
    ret = []
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)
        
        # discard areas that are too large
        if h>300 or w>300:
            continue

        # discard areas that are too small
        if h<15 or w<15:
            continue
            
        ret.append([x, y, w, h])
        
    ret = np.array(ret)
    #return ret #returns a list of [x, y, w, h] contour rectangles
    #'''
    contours = sorted(contours, key=lambda c: np.prod(cv2.boundingRect(c)[2:3]))

    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)
        
        # discard areas that are too large
        if h>300 or w>300:
            continue

        # discard areas that are too small
        if h<15 or w<15:
            continue
            
        # draw rectangle around contour on original image
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,0),2)

    # write original image with added contours to disk  
    cv2.imshow('contoured image', image)
    cv2.waitKey()
    
    #import sys
    cv2.destroyAllWindows()
    #sys.exit(0)
    #'''
    return ret #returns a list of [x, y, w, h] contour rectangles
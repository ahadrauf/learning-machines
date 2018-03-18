import cv2
import numpy as np

def detectText(image, dilationIterations = 3, displayImages = False):
    #2D filtering algorithm taken from: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
    #2D filtering blurs out noise while keeping important features (the features are also blurred, but they're still visible)
    kernel = np.ones((5,5),np.float32)/25
    processedImage = cv2.filter2D(image,-1,kernel)
	
    if (len(image.shape) > 2): #change the image to grayscale
        gray = cv2.cvtColor(processedImage,cv2.COLOR_BGR2GRAY)
    else: #the image was already grayscale
        gray = processedImage
		
    _, thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
    if displayImages:
        cv2.imshow('Threshold output, detectText', thresh)
        cv2.waitKey()
    
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))    
    dilated = cv2.dilate(thresh,kernel,iterations = dilationIterations) # dilate (the number of iterations is experimental, change if needed)
    if displayImages:
        cv2.imshow('Dilation output, detectText', dilated)
        cv2.waitKey()
    
    _, contours, _ = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours (i.e. regions where stuff is happening)
    ret = [] #contains all the valid contours (not too big/small)
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
    
    #undo all the comments below to stop drawing the graphics
    #return ret #returns a list of [x, y, w, h] contour rectangles
    #'''
    # for each contour found, draw a rectangle around it on original image
    for contour in ret:
        # get rectangle bounding contour
        [x,y,w,h] = contour
		
		# draw rectangle around contour on original image
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,0),2)

    # write original image with added contours to disk  
    if displayImages:
        cv2.imshow('contoured image', image)
        cv2.waitKey()
        cv2.destroyAllWindows()
    
    return ret #returns a list of [x, y, w, h] contour rectangles
	#'''
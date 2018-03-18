import numpy as np
import cv2
from matplotlib import pyplot as plt
from imutils.perspective import four_point_transform
from imutils import contours
import imutils

#Adapted from this post: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html
def findSubImage(image, contours, subimage):
    validContours = []
    for contour in contours:
        [x, y, w, h] = contour
        temp_image = image[y:y+h, x:x+w]
        good = findSubImageHelper(temp_image, subimage)
        if good > 0: # i.e. if there were matches
            validContours.append(([x, y, w, h], good))
    return sorted(validContours, key=lambda c: -c[1]) #sort contours in terms of number of matches, in decreasing order

def findSubImageHelper(image, subimage):    
    if image.shape[1] < 100:
        image = imutils.resize(image, height=100)
    
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(subimage,None)
    kp2, des2 = sift.detectAndCompute(image,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    if len(kp1) >= 2 and len(kp2) >= 2:
        matches = flann.knnMatch(des1,des2,k=2)
    else:
        matches = []

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
            
    return len(good)
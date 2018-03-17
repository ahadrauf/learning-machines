import numpy as np
import cv2
from matplotlib import pyplot as plt
from imutils.perspective import four_point_transform
from imutils import contours
import imutils

#MIN_MATCH_COUNT = 5
#import sys
    
def findSubImage(image, contours, subimage):
    validContours = []
    for contour in contours:
        [x, y, w, h] = contour
        temp_image = image[y:y+h, x:x+w]
        #temp_image = imutils.resize(temp_image, width=50)
        #print(temp_image.shape, x, y, w, h)
        #cv2.imshow('temp', temp_image)
        #cv2.waitKey()
        #cv2.imwrite('temp_image.jpg', temp_image)
        good = findSubImageHelper(temp_image, subimage)
        if good > 0: # i.e. if there were matches
            validContours.append(([x, y, w, h], good))
        #sys.stdout.flush()
    #os.remove('temp_image.jpg')
    return sorted(validContours, key=lambda c: -c[1])

def findSubImageHelper(image, subimage):    
    #subimage = cv2.GaussianBlur(subimage, (5, 5), 0)
    #_, subimage = cv2.subimage(subimage, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

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
    '''        
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = subimage.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        #image = cv2.polylines(image,[np.int32(dst)],True,0,3, cv2.LINE_AA)

    else:
        #print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
        matchesMask = None
    
    
    
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    img3 = cv2.drawMatches(subimage,kp1,image,kp2,good,None,**draw_params)
    plt.imshow(img3, 'gray'),plt.show()
    #plt.imshow(image, 'gray'), plt.show()
    '''
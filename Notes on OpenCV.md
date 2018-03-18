# Notes on OpenCV
OpenCV is a relatively versatile image processing tool, and it includes a lot of different functions that all have their own respective uses. Here, I've documented a few of the common code segments that I used in this project along with their common use cases.

## Basic OpenCV Functions
Note if you ever want to do work in OpenCV that it works around a backend of numpy, and all images and lists are stored as numpy.ndarray's. This is particularly important for data type management, since this can become a pain to debug when it goes wrong. Here are a few of the common OpenCV functions that come in handy when debugging/manipulating OpenCV images. For more details, consult [this more thorough list](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html)
* Displaying image shape. Because of the nature of grayscale vs. color images, it can be particularly important to verify this during your code, since a lot of OpenCV functions only work on grayscale images (you can do this with a cv2.COLOR_BGR2GRAY filter, which I'll get into below). Image shape is formatted as (row, column, num_channels), although for grayscale images the number of channels is by default 1.
```python
>>>print(grayscaleImg.shape)
(100,100)
>>>print(rgbImg.shape)
(100,100,3)
```
* Checking image type. This is another super-important thing to check if things go wrong for OpenCV, since a lot of OpenCV functions only accept uint8 images. This can be somewhat irritating, since a lot of image processing looks a lot nicer with uint64 images, and postconverting to a uint8 image sometimes just ends up looking worse than if you just used a uint8 image from the start, so be careful about this (note that if you start looking at the OpenCV source code in C++, you'll see a lot more variety of types like CV_8U1 or CV_8U3. You *hopefully* won't ever need to get involved with these):
```python
>>>print(img.dtype)
uint8
```

* Converting an image to grayscale. To do this, you need to change the color using the filter cv2.COLOR_BGR2GRAY (as you might guess, there's also a cv2.COLOR_GRAY2BGR to go from grayscale to color):
```python
processedImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

## Displaying Images
There were two common methods of displaying images that I used, one using openCV and one using matplotlib.
* OpenCV version. This is good for general image showing:
```python
import cv2
img = cv2.imread(file_path)
cv2.imshow('display_window_name', img) #shows the image in a pop-up window titled 'display_window_name'
cv2.waitKey() #pauses the code until you press any key (gives you time to look at the image)
cv2.destroyAllWindows() #optional, this deletes every image that was created using cv2.imshow() to this point
```

* matplotlib version. This is good if you want to display multiple images side-by-side:
```python
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread(file_path)
img2 = cv2.medianBlur(img, 5) #a sample filtering algorithm
plot_image = np.concatenate((img, img2), axis=0) #axis = 0 is on the vertical axis
plt.imshow(plot_image, 'gray') #plots in grayscale
plt.show()
```

## Filtering
In OpenCV (and image processing in general), filtering is another word for blurring (i.e. how much high-frequency noise can you blur out without damaging the rest of the image too much). For more details, check out this page by [OpenCV Python Tutorial](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html)

* 2D filtering: One of the fundamental low-pass filtering algorithms. It's great at blurring out noise, but it also is pretty bad with blurring out the rest of the image too (it turns out that this is great for detecting text, though):
```python
kernel = np.ones((5,5),np.float32)/25

processedImage = cv2.filter2D(img,-1,kernel) #convolves the kernel over the image
```

* Median Blur: One of the simpler algorithms, pretty fast but not very good if your image is taken with a camera (i.e. has uneven lighting conditions). It works pretty well for computer images or relatively uniform images, though.
```python
processedImage = cv2.medianBlur(5) #Increase the parameter -> more blurring
```

* Gaussian Blur: Similar to median blur, but pretty if you have uneven lighting conditions or images with lots of small features like text. Essentially, it's the same algorithm as median blur, but instead of blurring by using the median of the entire image as a reference value, it blurs by using the median of the immediate area (defined by the tuple you pass in) as its reference value.
```python
processedImg = cv2.GaussianBlur(img, (5, 5), 0)
```

## Thresholding
Thresholding is the last general OpenCV tool I'll get into here. Although there are a few different types of thresholding techniques (you can find a good tutorial [here](https://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html)). Fundamentally, it's used to convert grayscale images to more discrete black-and-white images for easier processing.

* Binary Thresholding: A relatively simple algorithm. If the pixel color is greater than a specified threshold, you make it the maximum value specified. Otherwise, you make it 0. Note that the second argument is the only one you'll actually need (the first one can be helpful such as for Otsu Thresholding (below), but you probably won't need it for most practical use):
```python
_, processedImg = cv2.threshold(grayscaleImg, threshold, maxValue, cv2.THRESH_BINARY)
```

* Binary Inverted Thresholding: The opposite of binary thresholding. If you'll note, I used this in the `textDetection.py` file because detecting white blobs (usually not very noisy) on a black background is easier than detecting black blobs on a white (but somewhat noisy) background.
```python
_, processedImg = cv2.threshold(grayscaleImg, threshold, maxValue, cv2.THRESH_BINARY_INV)
```

* Otsu Thresholding: This is a fancier version of thresholding where it learns the threshold parameter that best suits the image. This is nicer version to use in most occasions besides basic thresholding, but make sure to call other filtering algorithms like GaussianBlur beforehand to remove the differences in local lighting conditions and other random parameters. 
```python
_, processedImg = cv2.threshold(grayscaleImg, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
```

* Adaptive Thresholding: This is a fancier version of normal thresholding where it learns the threshold parameter based on the local area (defined by the two parameters at the end). Note that there are a lot of numbers to play around with, they all have their own effects so try it out and see :D ):
```python
processedImg = cv2.adaptiveThreshold(grayscaleImg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,13,6)
```
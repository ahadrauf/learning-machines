#ImageTextReader

This is an optical character recognition platform built specifically for medical equipment. 
Currently, it's designed to receive an input image of an equipment package (examples are found
in the folder `\examples`), from which it then parses out the lot number and expiration date,
two of the key identification components necessary to log and use medical equipment in standard
practice.

The software runs on OpenCV and PyTesser for image processing and character recognition, respectively.
* To install OpenCV (version 3.4.0 was used for this project), refer to 
[OpenCV-Python Tutorials](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html#install-opencv-python-in-windows)
for Windows and [PyImageSearch](https://www.pyimagesearch.com/2016/11/28/macos-install-opencv-3-and-python-2-7/) for macOS
* To install PyTesser (version 0.0.1 was used for this project), refer to 
[Google's PyTesser code archive](https://code.google.com/archive/p/pytesser/wikis/README.wiki). Note that you'll also need to install
Pillow in order to process images using PyTesser (you can install Pillow by following their 
[installation documentation](http://pillow.readthedocs.io/en/3.1.x/installation.html))

The code runs through the following steps:
1. Filter the image so it's more readable and at a standardized size
2. Use a smart cropping algorithm to isolate the desired portion of the image and remove the background
3. Find the active sections of the image (i.e. where *something* is going on, be it an image or text)
4. Check if there are any helpful tags in the image (for example, an hourglass symbol for the expiration date) to 
aid detection of important text
5. Parse through the active sections from step 3 while referring to the tags from step 4 to determine which regions 
contain the desired information
6. Parse out the desired information from the text in the desired active section, and output to console
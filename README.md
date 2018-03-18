#Image Text Reader

This is an optical character recognition platform built specifically for medical equipment. 
Currently, it's designed to receive an input image of an equipment package (examples are found
in the folder `\examples`), from which it then parses out the lot number and expiration date,
two of the key identification components necessary to log and use medical equipment in standard
practice.

The software runs on OpenCV and PyTesseract for image processing and character recognition, respectively.
* To install OpenCV (version 3.4.0 was used for this project), refer to 
[OpenCV-Python Tutorials](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html#install-opencv-python-in-windows)
for Windows and [PyImageSearch](https://www.pyimagesearch.com/2016/11/28/macos-install-opencv-3-and-python-2-7/) for macOS
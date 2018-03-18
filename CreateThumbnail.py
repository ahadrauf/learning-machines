from __future__ import print_function
#import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image

import main
import numpy as np
import argparse
import cv2
import imutils
from pytesser import *
     
#s3_client = boto3.client('s3')
     
#def resize_image(image_path, resized_path):
#    with Image.open(image_path) as image:
#        image.thumbnail(tuple(x / 2 for x in image.size))
#        image.save(resized_path)
     
def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key'] 
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/parsed-{}'.format(key)
        s3_client.download_file(bucket, key, download_path)
        date, log = main.parseImage(download_path)
        f = open(upload_path,"w+")
        f.write(date + "\n" + log)
        #s3_client.download_file(bucket, key, download_path)
        #resize_image(download_path, upload_path)        
        s3_client.upload_file(upload_path, '{}parsed'.format(bucket), key)
        
def handlerLocalTest(download_path, upload_path):
    #bucket = record['s3']['bucket']['name']
    #key = record['s3']['object']['key'] 
    #download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
    #upload_path = '/tmp/parsed-{}'.format(key)
    #s3_client.download_file(bucket, key, download_path)
    if os.path.exists(upload_path):
        os.remove(upload_path)
    date, log = main.parseImage(download_path)
    print('The item log number is', log)
    print('The expiration date is', date)
    sys.stdout.flush()
    f = open(upload_path,"w+")
    f.write(date + "\n" + log)
    #s3_client.download_file(bucket, key, download_path)
    #resize_image(download_path, upload_path)        
    #s3_client.upload_file(upload_path, '{}parsed'.format(bucket), key)
    
if __name__ == '__main__':
    #handlerLocalTest('examples/Webp.net-resizeimage.jpg', 'output.txt')
    handlerLocalTest('examples/sample_image1.jpg', 'output.txt')
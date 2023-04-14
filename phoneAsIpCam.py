import urllib.request
import cv2
import numpy as np

url = 'http://192.168.0.129:8080/shot.jpg'

while True:
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), np.uint8)
    img = cv2.imdecode(imgNp, -1)
    cv2.imshow('Phone', img)
    if ord('q') == cv2.waitKey(10):
     exit(0)
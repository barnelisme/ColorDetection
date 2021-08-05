# This is a sample Python script.


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 22222
Message = "0"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (50,50)
fontScale = 1
color = (0, 255, 0)
thickness = 2


img_width, img_height = 400, 300
dim = (img_width,img_height)

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("Value Min", "HSV", 0, 255, empty)
cv2.createTrackbar("Value Max", "HSV", 255, 255, empty)


# lower_blue = np.array([100,100,60])
# upper_blue = np.array([150,255, 200])



cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()
    # frame = cv2.GaussianBlur(hsv,(2,2),3)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Max", "HSV")
    s_max = cv2.getTrackbarPos("SAT Min", "HSV")
    v_min = cv2.getTrackbarPos("Value Min", "HSV")
    v_max = cv2.getTrackbarPos("Value Max", "HSV")

    lower_blue = np.array([h_min, s_min, v_min])
    upper_blue = np.array([h_max, s_max, v_max])

    print("lower_blue:" , lower_blue)



    #blur = cv2.blur(hsv, (3,3))

    #hsv = blur


    cv2.imshow("HSV Color", hsv)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    kernel = np.ones((5, 5), np.uint8)
    # closing = cv2.morphologyEx(hsv, cv2.MORPH_CLOSE, kernel)
    # hsv=closing


    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and(frame, frame, mask = mask)
    cv2.imshow('mask', mask)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]

    areas = [cv2.contourArea(c) for c in contours]
    # print(areas)
    cx = 0
    cy = 0
    try:
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        M = cv2.moments(cnt)
        # print(M)

        area = cv2.contourArea(cnt)

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        # print(area)
        print(cx, cy)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(hsv, (x, y), (x + w, y + h), (0, 255, 0), 2)

        Message = str(-(cx - 320) * (3.7 / 320))

        clientSocket.sendto(bytes(Message, 'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    except:
        clientSocket.sendto(bytes(Message, 'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
            # print("none exist")
        pass

    #frame = cv2.putText(hsv, str(str(cx) + "," + str(Message)), (cx, cy), font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("frame", frame)
    cv2.imshow("Result", result)

    cv2.waitKey(1)

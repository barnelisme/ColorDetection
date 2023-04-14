import cv2
import numpy as np
import argparse
import udpSend
import time
import socket
import threading

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (50, 50)
fontScale = 1
color = (0, 255, 0)
thickness = 2

framewidth = 640
frameheight = 480
# cap = cv2.VideoCapture("rtsp://192.168.8.119:554/Streaming/Channels/1")
# cap = cv2.VideoCapture("http://admin:0000@192.168.8.117/video/mjpg.cgi")
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)

cap.set(4, frameheight)

img1 = None

# stranger = cv2.bitwise_and(strangerOrg, strangerOrg, mask=fgmask)
# balls.append(ballUnit.BallBehaviour(framewidth,frameheight,1))

# print("From Function:",balls[0][0], balls[0])
UDP_IP1 = socket.gethostname()
UDP_PORT1 = 48901
UDP_IP2 = socket.gethostname()
UDP_PORT2 = 48902
#
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.bind((UDP_IP1, UDP_PORT1))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.bind((UDP_IP2, UDP_PORT2))

# Define a function for the thread
def Send_udp(name):
   delay = 2
   count = 0
   while True:
      #time.sleep(delay)
      count += 1
      print ("%s: %s" % ( name, time.ctime(time.time()) ))
      if sock1.recv is not None:
        data1, addr = sock1.recvfrom(1024)

        print("SensorTag[1] RSSIsTR:", str(data1))

def empty(a):
    pass
def BrightestSpot(img1):
    orig = img1.copy()
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False)
    ap.add_argument("-r", "--radius", type=int, help=3)
    args = vars(ap.parse_args())
    # perform a naive attempt to find the (x, y) coordinates of
    # the area of the image with the largest intensity value
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    cv2.circle(img1, maxLoc, 5, (255, 0, 0), 2)
    # display the results of the naive attempt
    cv2.imshow("Naive", img1)


def SpecificColor(img1):
    img = img1
    # imghsv = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    imghsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("Value Min", "HSV")
    v_max = cv2.getTrackbarPos("Value Max", "HSV")

    low_yellow_racket = np.array([26, 122, 178])
    up_yellow_racket = np.array([143, 174, 206])

    low_night_yellow_racket = np.array([23, 28, 184])
    up_night_yellow_racket = np.array([94, 127, 232])

    low_torch = np.array([1, 0, 255])
    up_torch = np.array([160, 5, 255])

    low_red_laser = np.array([141, 43, 157])
    up_red_laser = np.array([179, 222, 255])

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imghsv, low_red_laser, up_red_laser)
    result = cv2.bitwise_and(img, img, mask=mask)

    alpha = cv2.getTrackbarPos("alpha", "Transparency") / 10
    beta = cv2.getTrackbarPos("beta", "Transparency") / 10
    gamma = cv2.getTrackbarPos("gamma", "Transparency") / 10

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    hstack = np.hstack([img, mask, result])

    areas = [cv2.contourArea(c) for c in contours]

    # print("Areas:", areas)
    replace = img1
    try:
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        M = cv2.moments(cnt)
        # print(M)

        area = cv2.contourArea(cnt)

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        # print(area)
        # print(cx, cy)
        x, y, width, h = cv2.boundingRect(cnt)
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.rectangle(img, (x, y), (x + 50, y + 50), (0, 255, 0), 2)

        # Message = str(-(cx - 320) * (3.7 / 320))
        Message = str(cx) + ":" + str(frameheight - cy)
        print("Message:" + Message)
        udpSend.setMessage(Message)
        img = cv2.putText(img, "Player", (cx, cy), font, fontScale, color, thickness, cv2.LINE_AA)

        replace = img.copy()

    except Exception as e:
        # print("ERROR:", e)
        pass

    cv2.imshow('replace', replace)
    # cv2.imshow('Original', img)
    # cv2.imshow('Result Color Space', result)
    cv2.imshow('MASK Image', mask)
    # cv2.imshow('hstack', hstack)
    # cv2.imshow("frame", img)


cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("Value Min", "HSV", 0, 255, empty)
cv2.createTrackbar("Value Max", "HSV", 255, 255, empty)

cv2.namedWindow("Transparency")
cv2.resizeWindow("Transparency", 640, 240)
cv2.createTrackbar("alpha", "Transparency", 7, 20, empty)
cv2.createTrackbar("beta", "Transparency", 2, 20, empty)
cv2.createTrackbar("gamma", "Transparency", 0, 20, empty)



############ MAIN PROCESS #######################
try:
   thread1 = threading.Thread(target = Send_udp("LaserPointer"))
   thread1.start()

except Exception as err:
   print ("Error: unable to start thread" + err)
while True:
    try:
        _, img1 = cap.read()

        img = img1
    except Exception as err:
        print("Exception:" + str(err))

    #SpecificColor(img1)
    BrightestSpot(img1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


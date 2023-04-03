import cv2
import numpy as np
import udpSend
import checkPoint
import socket
import udpReceive
import RedImageValues

listOfPoints = []
incomingPoint = [0, 0]

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (50, 50)
fontScale = 1
color = (0, 255, 0)
thickness = 2

framewidth = 320
frameheight = 240

udpData = "Calibration"
activeScene = "Basic"

# cap = cv2.VideoCapture("rtsp://192.168.8.119:554/Streaming/Channels/1")
# cap = cv2.VideoCapture("http://admin:0000@192.168.8.117/video/mjpg.cgi")
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)

cap.set(4, frameheight)

xb = 120
yb = 50
x_mvmnt = "right"
y_mvmnt = "right"
# Radius of circle
radius = 20


# Blue color in BGR

# stranger = cv2.bitwise_and(strangerOrg, strangerOrg, mask=fgmask)
# balls.append(ballUnit.BallBehaviour(framewidth,frameheight,1))


# print("From Function:",balls[0][0], balls[0])
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

cv2.namedWindow("Transparency")
cv2.resizeWindow("Transparency", 640, 240)
cv2.createTrackbar("alpha", "Transparency", 7, 20, empty)
cv2.createTrackbar("beta", "Transparency", 2, 20, empty)
cv2.createTrackbar("gamma", "Transparency", 0, 20, empty)

size = 10
points = ["none"] * 10
pointsSize = len(points)

index = 1
writeIndex = 0
pointStatus = 0
i = 1

# Start of UDP Receive variable
# Create a Server Socket and wait for a client to connect

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setblocking(0)
server_socket.settimeout(0.0)
server_socket.bind(('', 55552))

while True:

# UDP RECEIVE CHECK POINT
    temp = udpReceive.ReceiveV2(server_socket)
    if "NONE" not in temp:
        if temp == "Calibration" or temp == "Reset" or temp == "Simulate":
            udpData = temp
        else:
            activeScene = temp

    print(temp)
# END OF UDP RECEIVE CHECK POINT

    try:
        _, img1 = cap.read()

        # cv2.imshow("Frame", img1)

        # Fliping the image
        # img = cv2.flip(img1, 1)
        img = img1
        
    except Exception as err:
        print("Exception:" + str(err))

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

    low_red = np.array([0, 144, 141])
    up_red = np.array([177, 255, 255])

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])


# CHECK NEW IMAGE PROCESSING VALUES ///////////
    valueResult = RedImageValues.findImgVAlues(activeScene)
    low_red_LIFE = valueResult[0]
    up_red_LIFE = valueResult[1]

# END OF CHECK NEW IMAGE PROCESSING VALUES ///

    mask = cv2.inRange(imghsv, low_red_LIFE, up_red_LIFE)
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
        incomingPoint = [cx, (frameheight - cy)]  # save the new incoming point
        tempString = " "

        if udpData == "Calibration":
            udpSend.broadcastMessage(Message)
            # print("Message sent is: " + Message)
        else:
            shouldWeSendNewPoint = checkPoint.checkNewPoint(incomingPoint, listOfPoints)

        if udpData == "Reset":
            listOfPoints = []

        if shouldWeSendNewPoint:
            udpSend.broadcastMessage(Message)
            listOfPoints.append(incomingPoint)  # add the point in the list
            # now we need to find a way to reset the list from unity

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

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


import cv2
import numpy as np
import socket
import threading
import time
import udpReceive
import checkPoint
import checkPointInTree

# UDP settings
UDP_IP = '127.0.0.1'  # Replace with the IP address of your UDP receiver
UDP_PORT = 22222
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IGNORE_RADIUS = 2

framewidth = 320
frameheight = 240

#UDP Receive Variables
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setblocking(0)
server_socket.settimeout(0.0)
server_socket.bind(('', 55552))

listOfPoints = [[0,0],[0,1]]
incomingPoint = [0,0]
# Create an empty dictionary to store points
point_dict = {}

# Function to send coordinates via UDP
def send_coordinates(coordinates):
    #message = f"{coordinates[0]},{coordinates[1]}"
    #sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # print("Broadcasting")

    sock.sendto(bytes(str(coordinates), "utf-8"), ("255.255.255.255", 22222))


def checkStartCondition():   #udp for receiving the start camera condition
    cameraOption = " "
    
    while True:
        temp = udpReceive.ReceiveV2(server_socket)
        
        if temp == "Camera 0" or temp == "Camera 1":
            cameraOption = temp
            break

        #print("temp 1 is" + temp)
    return cameraOption


def receive_UDP(udpDataStr, simSettingStr):    #udp for data and active scene names
    
    temp = udpReceive.ReceiveV2(server_socket)
    #print("temp 2 is" + temp)
    if temp == "Calibration" or temp == "Reset" or temp == "Simulate" or temp == "Calibrate":
        udpDataStr = temp
    if temp == "Live" or temp == "Laser" or temp == "Game":
        simSettingStr = temp
     
    return udpDataStr, simSettingStr


def process_stream():
    
    global is_CheckUdp
    functionEndpoint = 1
    videoCapVal = 0
    cameraOption = " "
    cameraOptMsg = " "
    
    udpData = "empty"
    simSetting = "empty"
    is_CheckUdp = "true"
    start = " "
    listOfPoints = [ ]
    incomingPoint = [0, 0]

    #////////////////////////CHECK CAMERA OPTION//////////////////////
    #/////////////////////////////////////////////////////////////////
    print("Please select camera option")
    print("...")
    cameraOption = checkStartCondition()
    
    if cameraOption == "Camera 0":
        videoCapVal = 0
        cameraOptMsg = "default"
        if functionEndpoint != 0:      #Condition for running the code once
            print("Opening " + cameraOptMsg + " camera.")
            cap = cv2.VideoCapture(videoCapVal)
            functionEndpoint = 0
            
    elif cameraOption == "Camera 1":
        videoCapVal = 1
        cameraOptMsg = "exterior"
        if functionEndpoint != 0:      #Condition for running the code once
            print("Opening " + cameraOptMsg + " camera.")
            cap = cv2.VideoCapture(videoCapVal)
            functionEndpoint = 0
    #/////////////////////////////////////////////////////////////////
    #////////////////////////END OF CHECK/////////////////////////////
                
    
    global frameInit
    # Initialize the USB camera
    cap.set(3, framewidth)
    cap.set(4, frameheight)

    # Create a window with a slider bar to adjust the threshold value
    window_name = 'Threshold'
    cv2.namedWindow(window_name)
    cv2.createTrackbar('Value', window_name, 250 , 255, lambda x: None) #Mall
    current_value = cv2.getTrackbarPos('Value', window_name)
    global trackBarSwitch
    trackBarSwitch = 0

    # Initialize a list to store all previously detected points
    previous_points = []

    while functionEndpoint == 0:

        try:
            #print("Running Camera")
            #//////////////////////////////////////////
            
            if is_CheckUdp == "true":
                temp = receive_UDP(udpData, simSetting)
                tempData = temp[0]
                tempSetting = temp[1]
                udpData = tempData
                simSetting = tempSetting

            
            #//////////////////////////////////////////
            if "Calibrate" in udpData:
                trackBarSwitch = 1

            if trackBarSwitch == 1:
                if "Calibrate" in udpData:
                    cv2.setTrackbarPos('Value', window_name, 210)
                if "Calibrate" not in udpData:
                    cv2.setTrackbarPos('Value', window_name, current_value)
                    trackBarSwitch = 0
            if trackBarSwitch == 0:
                current_value = cv2.getTrackbarPos('Value', window_name)
                #if "NONE" not in temp:
                if "Indoor" in simSetting:
                    cv2.setTrackbarPos('Value', window_name, current_value)
                if "Basic" in simSetting:
                    cv2.setTrackbarPos('Value', window_name, current_value)


            #print(trackBarSwitch)
            #print(udpData)

            # Read a frame from the camera
            ret, frame = cap.read()
            frameInit = frame

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Get the current threshold value from the slider bar
            threshold_value = cv2.getTrackbarPos('Value', window_name)

            # Threshold the grayscale image to get all points above the current threshold value
            ret, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

            # Find the contours of the thresholded image
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            areas = [cv2.contourArea(c) for c in contours]  ##Branch of the UDP send X variables

            # if (current_value is not cv2.getTrackbarPos('Value', window_name)) or "Calibration" in udpData:
            # Add the new point to the list of previous points

            # Draw a blue circle around each contour and send its coordinates via UDP
            for contour in contours:
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)

                # Variables for UDP Send Cordinates
                max_index = np.argmax(areas)
                cnt = contours[max_index]
                M = cv2.moments(cnt)

                # Check if the new point is within 2 pixels of any previous point
                point_exists = False
                if not point_exists:
                    # Draw a blue circle around the new point
                    cv2.circle(frame, center, radius, (255, 0, 0), 2)

                incomingPoint = [x, (frameheight - y)]  # save the new incoming point
                center_UDP = str(int(x)) + ":" + str(frameheight - int(y))

                if simSetting == "Live":

                    if udpData == "Calibration":
                        send_coordinates(center_UDP)
                        # print("Message sent is: " + Message)
                    else:
                        shouldWeSendNewPoint = checkPointInTree.checkNewPoint(incomingPoint, listOfPoints)

                    if udpData == "Reset":
                        listOfPoints = []

                    if shouldWeSendNewPoint:
                        send_coordinates(center_UDP)
                        # listOfPoints.append(incomingPoint)  # add the point in the list
                        # now we need to find a way to reset the list from unity
                else:
                    send_coordinates(center_UDP)


            # Display the frame and slider bar
            cv2.imshow(window_name, thresh)
            cv2.imshow('frame', frame)

            # Check for key press and exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as err:
            #print("Exception:" + str(err))
            pass



    # Release the camera and close the windows
    cap.release()
    cv2.destroyAllWindows()


# Define the function to generate the video stream for Flask
def generate():
    global frameInit
    #while True:
    if frameInit is not None:
            ret, jpeg = cv2.imencode('.jpg', frameInit)
            frameInit = None
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


if __name__ == '__main__':

    global cameraOption, videoCapVal, cameraOptMsg
    
    
    # Start the video stream processing in a separate thread
    threading.Thread(target=process_stream).start()
    # Start the Flask server in a separate thread
    #threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': False}).start()
    #threading.Thread(target=checkStartCondition()).start()

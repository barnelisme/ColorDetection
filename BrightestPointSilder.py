import cv2
import numpy as np
import socket
import threading
import time
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from flask import app, Flask
from werkzeug import Response

app = Flask(__name__)
frameInit = None

# UDP settings
UDP_IP = '127.0.0.1'  # Replace with the IP address of your UDP receiver
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IGNORE_RADIUS = 2

# Function to send coordinates via UDP
def send_coordinates(coordinates):
    message = f"{coordinates[0]},{coordinates[1]}"
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

def process_stream():
    global frameInit
    # Initialize the USB camera
    cap = cv2.VideoCapture(0)

    # Create a window with a slider bar to adjust the threshold value
    window_name = 'Threshold'
    cv2.namedWindow(window_name)
    cv2.createTrackbar('Value', window_name, 240, 255, lambda x: None)

    # Initialize a list to store all previously detected points
    previous_points = []

    while True:
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

        # Draw a blue circle around each contour and send its coordinates via UDP
        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)

            # Check if the new point is within 2 pixels of any previous point
            point_exists = False
            ''' if(previous_points.__contains__([center])):
                point_exists = True
                print("Valid")
            else:
                point_exists = False
                print("Skip")'''

            for previous_point in previous_points:
                try:
                    if np.linalg.norm(np.array(previous_point) - np.array(center)) < IGNORE_RADIUS:
                        point_exists = True
                        break
                except:
                    pass

            if not point_exists:
                # Draw a blue circle around the new point
                cv2.circle(frame, center, radius, (255, 0, 0), 2)

                # Send the new point's coordinates via UDP
                send_coordinates(center)

                # Add the new point to the list of previous points
                previous_points.append(center)
            else:
                print("Point already exist.")

            # Remove each point from the list after 5 seconds
            try:
                current_time = time.time()
                previous_points = [previous_point for previous_point in previous_points if current_time - previous_point[2] <= 5]
            except:

                pass

        # Add the current time to each point in the list of previous points
        previous_points = [(previous_point[0], previous_point[1], time.time()) for previous_point in previous_points]

        # Display the frame and slider bar
        cv2.imshow(window_name, thresh)
        cv2.imshow('frame', frame)

        # Check for key press and exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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

# Define the Flask route to expose the video stream
@app.route('/')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the video stream processing in a separate thread
    threading.Thread(target=process_stream).start()
    # Start the Flask server in a separate thread
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': False}).start()

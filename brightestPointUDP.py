import cv2
import numpy as np
import socket
import threading
from flask import Flask, Response

app = Flask(__name__)
frame = None

# Define the UDP server and port
UDP_IP = '127.0.0.1'
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)

# Define the function to send the coordinates via UDP
def send_udp(x, y):
    data = str(x) + ',' + str(y)
    sock.sendto(data.encode(), (UDP_IP, UDP_PORT))

# Define the function to process the video stream
def process_stream():
    global frame
    # Define the capture device (in this case, the USB camera)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert the frame to gray scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply a threshold to the gray scale image
        ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        # Find the contours in the thresholded image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Draw a blue circle around all points above 240
        for contour in contours:
            M = cv2.moments(contour)
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                if gray[cy, cx] > 240:
                    cv2.circle(frame, (cx, cy), 10, (255, 0, 0), -1)
                    print("cx:"+ str(cx) + ", cy=" + str(cy))
                    # Send the coordinates via UDP
                    threading.Thread(target=send_udp, args=(cx, cy)).start()

# Define the function to generate the video stream for Flask
def generate():
    global frame
    while True:
        if frame is not None:
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = None
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

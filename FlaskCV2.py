import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)

# OpenCV's VideoCapture object to read video frames
cap = cv2.VideoCapture(0)  # 0 is the default camera index

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        # Read frame from the camera
        success, frame = cap.read()

        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)

            # Convert the image data to a byte array and yield it as a chunk of data
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '_main_':
    app.run(debug=True)
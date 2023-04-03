from flask import Flask, Response
import VideoCapture

app = Flask(__name__)

@app.route("/")
def home():
    #return  VideoCapture.Video_capture()
    return Response(VideoCapture.Video_capture(), mimetype='multipart/x-mixed-replace; boundary=frame')

    return "Hello world, from Flask Generator!"

if __name__ == '__main__':
    app.run(host="192.168.0.102")

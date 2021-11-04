from flask import Flask, render_template, abort, request, redirect, url_for, Response
from flask_caching import Cache
import cv2
from blink_detection import face_detection
import sys

config = {
    "DEBUG": True,                # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)

@app.route('/')
def index():
    return render_template('baseExt.html')

@app.errorhandler(404)
def open_dreampage(error):
    return redirect(url_for('index')), 404

# generate frame by frame from camera
def gen_frames():
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            eye_open, frame = face_detection(frame, face_cascade, eye_cascade)
            cache.set("eye_open", eye_open)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.get('/video_feed')
def video_feed():
    print('video feed!', file=sys.stdout)
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# generate frame by frame from two images
def get_image():
    while True:
      if cache.get("eye_open"):
        img = eye_open_img
      else:
        img = eye_close_img
      yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+ img + b'\r\n')

@app.get("/img_feed")
def img_feed():
    print('display eye!', file=sys.stdout)
    return Response(get_image(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/<path:path>')
def open_paths(path):
  if path == 'p1':
    return render_template('p1Ext.html')
  elif path == 'forecast':
    return render_template('forecastExt.html')
  elif path == 'whitehole':
    return render_template('whiteholeExt.html')
  else:
    abort(404)

if __name__ == '__main__':
    cache = Cache(app)
    cache.set("eye_open", True)
    camera = cv2.VideoCapture(0)  # web camera

    # init the face and eye cascade classifiers from xml files
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    eye_open_img = open('static/img/open.png', 'rb').read()
    eye_close_img = open('static/img/close.png', 'rb').read()
    
    app.run(debug=True)
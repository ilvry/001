from flask import Flask, render_template, abort, request, redirect, url_for, Response, jsonify
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect
import cv2
import json
from blink_detection import face_detection

config = {
    "DEBUG": True,                # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('baseExt.html')

@app.errorhandler(404)
def open_dreampage(error):
    return redirect(url_for('index'))

@csrf.exempt
@app.route('/getFrame', methods=['GET'])
def get_frame():
  if request.method == "GET":
    # Capture frame-by-frame
    success, frame = camera.read()  # read the camera frame
    if success:
      eye_open, frame = face_detection(frame, face_cascade, eye_cascade)
      return jsonify({'eyestatus': eye_open})
    else:
      return jsonify({'error': 'failed to reach camera'})
  return jsonify({'error': 'wrong request type'})

@app.route('/<path:path>')
def open_paths(path):
  if path == 'p1':
    return render_template('p1Ext.html')
  elif path == 'water':
    return render_template('waterExt.html')
  elif path == 'forecast':
    return render_template('forecastExt.html')
  elif path == 'whitehole':
    return render_template('whiteholeExt.html')
  else:
    abort(404)

if __name__ == '__main__':
    camera = cv2.VideoCapture(0)  # web camera

    # init the face and eye cascade classifiers from xml files
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    eye_open_img = open('static/img/open.png', 'rb').read()
    eye_close_img = open('static/img/close.png', 'rb').read()
    
    app.run(debug=True)
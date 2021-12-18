from flask import Flask, render_template, abort, request, redirect, url_for, Response, jsonify
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect
import cv2
import json
from blink_detection import eye_detection, face_detection

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

#@csrf.exempt
#@app.route('/getFrame', methods=['GET'])
#def get_frame():
#  if request.method == "GET":
#    # Capture frame-by-frame
#    success, frame = camera.read()  # read the camera frame
#    if success:
#      eye_open, frame = eye_detection(frame, face_cascade, eye_cascade)
#      return jsonify({'eyestatus': eye_open})
#    else:
#      return jsonify({'error': 'failed to reach camera'})
#  return jsonify({'error': 'wrong request type'})

@app.route('/<path:path>')
def open_paths(path):
  if path == 'p1':
    return render_template('p1Ext.html')
  elif path == 'water':
    return render_template('waterExt.html')
  elif path == 'forecast':
    return render_template('forecastExt.html')
  elif path == 'ripple':
    return render_template('rippleExt.html')
  elif path == 'whitehole':
    return render_template('whiteholeExt.html')
  else:
    abort(404)
    
# generate frame by frame from camera
def gen_frames():
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            eye_open, frame = eye_detection(frame, face_cascade, eye_cascade)
            cache.set("eye_open", eye_open)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# generate frame by frame from two images
def get_image():
    while True:
      if cache.get("eye_open") == "open":
        img = eye_open_img
      else:
        img = eye_close_img
      yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+ img + b'\r\n')

@app.route("/img_feed")
def img_feed():
    return Response(get_image(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/water_feed')
def water_feed():
  # Capture frame-by-frame
  success, frame = camera.read()  # read the camera frame
  if not success:
      return water_i_drop_vid
  else:
    watched, frame = face_detection(frame, face_cascade)
    if watched:
      return water_i_drop_2_vid
    else:
      return water_i_drop_vid


if __name__ == '__main__':
    cache = Cache(app)
    cache.set("eye_open", "open")
    camera = cv2.VideoCapture(0)  # web camera

    # init the face and eye cascade classifiers from xml files
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    eye_open_img = open('static/img/open.png', 'rb').read()
    eye_close_img = open('static/img/close.png', 'rb').read()
    
    water_i_drop_vid = open('static/vid/water_i_drop.mp4', 'rb').read()
    water_i_drop_2_vid = open('static/vid/water_i_drop_2.mp4', 'rb').read()
    
    app.run(debug=True)

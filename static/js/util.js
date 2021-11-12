localStorage.setItem('eyeopen', 'open');
var eye_open_img = 'static/img/open.png'
var eye_close_img = 'static/img/close.png'

// retrieve latest weather from api once every minute
function getCurrEye(){
  var eye_state = localStorage['eyeopen'];
  var img = eye_open_img;
  if (eye_state == 'close') {
    img = eye_close_img 
  }
  document.getElementById('curr-eye-img').src=img;
  document.getElementById('curr-eye-img').style="width:50%;bottom:100px;"; 
  setTimeout(getCurrEye, 5);
};
getCurrEye();

function onOpenCvReady(){
  console.log('OpenCV ready', cv);
  cv.onRuntimeInitialized=()=>{
    var dst = new cv.Mat(720, 1280, cv.CV_8UC4);
    const FPS = 50;
    function processVideo() {
      try {
        var begin = Date.now();
        // start processing frame.
        $.ajax({
          type: "GET",
          url: "/getFrame",
          success: function(output){
            console.log(output);
          },
          dataType: "json",
          contentType: "application/json",
          error: function (request, error) {
            console.log("get video processing results failed");
          }
        }).done(function(data){
          if (data.error) {
            console.log(data.error);
          } else {
            if (data.eyestatus) {
              console.log(data.eyestatus);
              localStorage.setItem('eyeopen', data.eyestatus);
              getCurrEye();
            }
            // Uncomment the following to get video demension.
            // console.log(data.length, data[0].length, data[0][0].length);

            // schedule the next one.
            var delay = 1000/FPS - (Date.now() - begin);
            setTimeout(processVideo, delay);
          }
        });
      } catch (err) {
        console.log("video display failed");
      }
    };

    // schedule the first one.
    setTimeout(processVideo, 0);
  };
}

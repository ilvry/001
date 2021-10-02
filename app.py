from flask import Flask, render_template, abort
app = Flask(__name__)

@app.route('/')
def open_mainpage():
    return render_template('baseExt.html')
  
@app.route('/<path:path>')
def open_paths(path):
  if path == 'p1':
    return render_template('p1Ext.html')
  else:
    abort(404)

@app.errorhandler(404)
def open_dreampage(error):
    return render_template('baseExt.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
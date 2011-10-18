#!/usr/bin/env python2

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/art/<slidefile>')
def slideshow(slidefile):
  return render_template('slides.html', slide=slidefile)

if __name__ == '__main__':
  app.run(debug = True)


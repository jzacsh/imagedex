#!/usr/bin/env python2

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/art/')
@app.route('/art/<slidefile>')
def slideshow(slidefile=None):
  return render_template('slides.html', data = {
      'title': "Jonathan Zacsh's Drawings",
      'slide': slidefile,
      })

if __name__ == '__main__':
  app.run(debug = True)


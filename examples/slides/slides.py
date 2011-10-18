#!/usr/bin/env python2

from flask import Flask
app = Flask(__name__)

@app.route('/art')
def slideshow():
  return "Slideshow coming soon..."

if __name__ == '__main__':
  app.run(debug = True)


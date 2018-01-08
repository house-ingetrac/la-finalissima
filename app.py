import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import urllib2, json


app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def root():
    #if 'user' in session:
    return render_template('map.html', title = "Map")
    #else:
     #   return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/map')
def map():
    return render_template('map.html', title = "Map")

if __name__ == '__main__':
    app.debug = True
    app.run()


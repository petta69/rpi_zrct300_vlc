#!/bin/python3

import sys
import os
from flask import Flask, render_template, request, url_for, redirect


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
import vlc_app
import zrct300_app


## This is a comment
@app.route('/')
def index():
    return render_template('index.html')




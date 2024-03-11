from app import app
from flask import Flask, render_template, request

@app.route('/zrct300')
def zrct300():
    return render_template('zrct300.html')

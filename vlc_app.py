from app import app
from flask import Flask, render_template, request

import video_player

Player = video_player.player()

@app.route('/vlc')
def vlc():
    return render_template('vlc.html', vlc=Player.is_initiated)

@app.route('/vlcPlayDefaultList')
def vlcPlayDefaultList():
    Player.play_default_list()
    return render_template('vlc.html', vlc=Player.is_initiated)

@app.route('/vlcPlay')
def vlcPlay():
    Player.play()
    return render_template('vlc.html', vlc=Player.is_initiated)

@app.route('/vlcPause')
def vlcPause():
    Player.pause()
    return render_template('vlc.html', vlc=Player.is_initiated)

@app.route('/vlcPrev')
def vlcPrev():
    Player.prev()
    return render_template('vlc.html', vlc=Player.is_initiated)

@app.route('/vlcNext')
def vlcNext():
    Player.next()
    return render_template('vlc.html', vlc=Player.is_initiated)

@app.route('/vlcHelp')
def vlcHelp():
    vlc_help = Player.help()
    return render_template('vlc.html', vlc=Player.is_initiated, vlc_help=vlc_help)

@app.route('/vlcTitle')
def vlcTitle():
    vlc_title = Player.get_title()
    return render_template('vlc.html', vlc=Player.is_initiated, vlc_info=vlc_title)

@app.route('/vlcPlaylist')
def vlcPlaylist():
    vlc_playlist = Player.playlist()
    return render_template('vlc.html', vlc=Player.is_initiated, vlc_info=vlc_playlist)

@app.route('/vlcInfo')
def vlcInfo():
    vlc_info = Player.info()
    return render_template('vlc.html', vlc=Player.is_initiated, vlc_info=vlc_info)

@app.route('/vlcStatus')
def vlcStatus():
    vlc_status = Player.status()
    return render_template('vlc.html', vlc=Player.is_initiated, vlc_status=vlc_status)

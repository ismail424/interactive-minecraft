#flask
from re import M
from flask import Flask, render_template, request, redirect, url_for, sessions, session
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.utils import import_string
from flask_socketio import SocketIO, emit
from functions import *
import os
import re
import json
from mctools import RCONClient 
import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

with open('config.json', 'r') as f:
    config = json.load(f)
    
RCON_IP = config['rcon_ip']
RCON_PASSWORD = config['rcon_password']
RCON_PORT = config['rcon_port']

rcon = RCONClient(RCON_IP, port=RCON_PORT)

all_users = []

@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/join', methods=['POST'])
def join():
    global all_users
    
    if session.get('username'):
        return redirect(url_for('dashboard'))
    
    username = request.form.get('username')
    username = username.strip()
    username = username.replace(" ", "")
    if len(username) < 3:
        print("Username too short")
        return redirect(url_for('index'))
    if len(username) > 15:
        username = username[:15]
    for user in all_users:
        if user['username'] == username:
            return render_template('login.html', error='Username already taken, choose another username!')
    
    random_token = random_string(15)
    all_users.append({"token": random_token, "username": username, "points": 0})
    
    session["username"] = username
    session["token"] = random_token
    usernames = get_all_usernames()
    socketio.emit('all_users', usernames)
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    global all_users
    if check_user(session, all_users):
        username = session.get('username')
        status = check_server_status(rcon, RCON_PASSWORD)
        online_mc_players = online_minecraft_players()
        if len(online_mc_players) == 0:
            online_mc_players = False
        user_info = get_user_by_username(all_users,username)

        return render_template('dashboard.html', user_info=user_info,status=status, online_mc_players=online_mc_players)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    global all_users
    remove_from_list(all_users, session.get('username'))
    session.pop('username', None)
    session.pop('token', None)
    usernames = get_all_usernames()
    socketio.emit('all_users', usernames)
    return redirect(url_for('index'))

@app.route('/all_users')
def check_all_users():
    global all_users
    usernames_from_all_users = []
    for user in all_users:
        usernames_from_all_users.append(user['username'])
    return json.dumps(usernames_from_all_users)

@app.route('/commands')
def commands():
    global all_users
    if check_user(session, all_users):
        user_info = get_user_by_username(all_users, session.get('username'))
        with open('commands.json', 'r') as f:
            all_commands = json.load(f)
        return render_template('commands.html',user_info=user_info, all_commands=all_commands)
    return redirect(url_for('index'))

@app.route('/potions')
def potions():
    global all_users
    if check_user(session, all_users):
        user_info = get_user_by_username(all_users, session.get('username'))
        return render_template('potions.html',user_info=user_info)
    return redirect(url_for('index'))

@app.route('/weather')
def weather():
    global all_users
    if check_user(session, all_users):
        user_info = get_user_by_username(all_users, session.get('username'))
        return render_template('weather.html',user_info=user_info)
    return redirect(url_for('index'))

def get_all_usernames():
    global all_users
    usernames = []
    for user in all_users:
        usernames.append(user['username'])
    return usernames

@socketio.on("mc-command")
def run_mc_command(data):
    try:
        global all_users
        username = str(data["username"])
        command_id = int(data["command_id"])
        for user in all_users:
            if user["username"] == username:
                current_user_points = user["points"]
        
        command = get_command_by_id(command_id)
        points = get_points_by_id(command_id)
        if current_user_points >= points:
            if command:
                run_command(command)
            remove_points(username, points)
     
    except Exception as e:
        import sys
        print("Error")
        print(e)
        print(data)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        pass

@socketio.on('get_all_users')
def update_all_users():
    usernames = get_all_usernames()
    emit('all_users', usernames)

def run_command(command: str):
    try:
        if rcon.login(RCON_PASSWORD):
            resp = rcon.command(command)
        return resp
    except Exception as e:
        print(e)
        return e
    
#Fetch minecraft profile picture API
def get_profile_picture(username: str):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        response = requests.get(url)
        response = response.json()
        uuid = response['id']
        url = f"https://crafatar.com/avatars/{uuid}?overlay"
        return url, uuid
    except Exception as e:
        print(e)
        uuid = "0"
        url = "https://crafatar.com/avatars/1?overlay"
        return url, uuid
    
def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

def online_minecraft_players():
    mc_players = run_command("list")
    mc_players = mc_players.split("online: ")[1]
    mc_players = escape_ansi(mc_players)
    if mc_players != "":
        mc_players = mc_players.split(", ")
        new_minecraft_players = []    
        for player in mc_players:                                           
            player = player.replace("\x1b[0m", "")
            avatar, uuid = get_profile_picture(player)
            new_minecraft_players.append({"username": player, "uuid": uuid, "avatar": avatar})
        return new_minecraft_players
    else:
        return []

#Run this function every 5 seconds
def add_points():
    global all_users    
    for user in all_users:
        user["points"] += 10
        socketio.emit('points', {'points': user["points"], 'username': user["username"]})
        
def remove_points(username:str, points:int):
    global all_users
    for user in all_users:
        if user["username"] == username:
            user["points"] -= points
            socketio.emit('points', {'points': user["points"], 'username': user["username"]})

if __name__ == "__main__":
    sched = BackgroundScheduler()
    sched.add_job(func=add_points,trigger='interval',seconds=5)
    sched.start()
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
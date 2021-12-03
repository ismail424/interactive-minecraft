#flask
from re import M
from flask import Flask, render_template, request, redirect, url_for, sessions, session
from flask_socketio import SocketIO, emit
from functions import *
import os
import json
from mctools import RCONClient 
import requests

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
user_points = 0

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
    if len(username) > 15:
        username = username[:15]
    for user in all_users:
        if user['username'] == username:
            return render_template('login.html', error='Username already taken, choose another username!')
    
    random_token = random_string(15)
    all_users.append({"token": random_token, "username": username})
    
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
        return render_template('dashboard.html', username=username, user_points=user_points, status=status, online_mc_players=online_mc_players)
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
    return render_template('commands.html')

@app.route('/potions')
def potions():
    return render_template('potions.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

def get_all_usernames():
    global all_users
    usernames = []
    for user in all_users:
        usernames.append(user['username'])
    return usernames

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
        return "error"
    
#fetch minecraft profile picture api
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
    
def online_minecraft_players():
    mc_players = run_command("list")
    mc_players = mc_players.replace("There are 1 of a max of 20 players online:", "")
    new_minecraft_players = []
    print(mc_players)
    # for player in mc_players:                                           
    #     player = player.replace("\x1b[0m", "")
    #     avatar, uuid = get_profile_picture(player)
    #     new_minecraft_players.append({"username": player, "uuid": uuid, "avatar": avatar})
    return new_minecraft_players
if __name__ == "__main__":
    online_minecraft_players()
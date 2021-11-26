#flask
from flask import Flask, render_template, request, redirect, url_for, sessions, session
from flask_socketio import SocketIO, emit
from functions import *
import os
import json
from mctools import RCONClient 

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
    if session.get('username'):
        return redirect(url_for('dashboard'))
    global all_users
    username = request.form.get('username')
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
    if session.get('username'):
        username = session.get('username')
        if session.get('token'):
            token = session.get('token')
            for user in all_users:
                if user['username'] == username and user['token'] == token:
                    return render_template('dashboard.html', username=username)
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
    
if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')
#flask
import flask
from flask import Flask, render_template, request, redirect, url_for, sessions, session
from flask_socketio import SocketIO, emit
from functions import *
import os
import json
    
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

all_users =[]

@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
    if session.get('username'):
        return redirect(url_for('dashboard'))
    global all_users
    username = request.form.get('username')
    for user in all_users:
        if user['username'] == username:
            return render_template('index.html', error='Username already taken, choose another username!')
    
    random_token = random_string(15)
    all_users.append({"token": random_token, "username": username})
    
    session["username"] = username
    session["token"] = random_token
    
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
    return redirect(url_for('index'))

@app.route('/all_users')
def check_all_users():
    global all_users
    usernames_from_all_users = []
    for user in all_users:
        usernames_from_all_users.append(user['username'])
    return json.dumps(usernames_from_all_users) 

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')
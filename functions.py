import random
import string

def random_string(length):
    return str(''.join(random.choice(string.ascii_letters) for i in range(length)))

def remove_from_list(list, username):
    for user in list:
        if user['username'] == username:
            list.remove(user)
            return
        
def check_user(session, all_users):
    if session.get('username'):
        username = session.get('username')
        if session.get('token'):
            token = session.get('token')
            for user in all_users:
                if user['username'] == username and user['token'] == token:
                    return True
    return False

def check_server_status(rcon, RCON_PASSWORD):
    try:
        if rcon.login(RCON_PASSWORD):
            resp = rcon.command("list")
            return True
        else:
            return False
    except:
        return False

    
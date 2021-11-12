import random
import string

def random_string(length):
    return str(''.join(random.choice(string.ascii_letters) for i in range(length)))

def remove_from_list(list, username):
    for user in list:
        if user['username'] == username:
            list.remove(user)
            return
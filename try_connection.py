from mctools import RCONClient 
import json

with open('config.json', 'r') as f:
    config = json.load(f)
    
RCON_IP = config['rcon_ip']
RCON_PASSWORD = config['rcon_password']
RCON_PORT = config['rcon_port']

rcon = RCONClient(RCON_IP, port=RCON_PORT)

if rcon.login(RCON_PASSWORD):
    resp = rcon.command("list")
    print(resp)
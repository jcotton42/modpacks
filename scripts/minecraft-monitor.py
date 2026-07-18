#!/usr/bin/python3

import json
import os
import subprocess
import urllib.parse
import urllib.request

MESSAGE_LIMIT = 1024
LOWEST = -2
LOW = -1
NORMAL = 0
HIGH = 1

PUSHOVER_API_TOKEN = os.getenv('PUSHOVER_API_TOKEN')
PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')
CONTAINERS_TO_WATCH = os.getenv('CONTAINERS_TO_WATCH').split(',')

def send_pushover(title, message, timestamp, *, priority=LOW):
    data = urllib.parse.urlencode({
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message[:MESSAGE_LIMIT],
        "priority": priority,
        "timestamp": timestamp,
    }).encode("utf-8")
    urllib.request.urlopen("https://api.pushover.net/1/messages.json", data=data)

podman = subprocess.Popen(
    ['podman', 'events', '--filter=type=container', '--format', 'json', '--stream'],
    stdout=subprocess.PIPE,
    bufsize=1,
    text=True)

for line in podman.stdout:
    event = {k.lower(): v for k, v in json.loads(line).items()}
    if event['status'] != 'died':
        continue

    name = event['name']
    exit_code = event['containerexitcode']
    timestamp = event['time']
    print(f'{name} at {timestamp} with {exit_code}')
    if name not in CONTAINERS_TO_WATCH:
        continue

    if exit_code == 0:
        send_pushover(f'{name} exited', f'{name} exited normally', timestamp, priority=LOWEST)
    else:
        send_pushover(f'{name} exited abnormally', f'{name} exited with an exit code of {exit_code}', timestamp, priority=NORMAL)

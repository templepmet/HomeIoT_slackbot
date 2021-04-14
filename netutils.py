import time
import socket
import netifaces
import subprocess
import slackbot_settings
from wakeonlan import send_magic_packet

def get_ip():
    try:
        ip = netifaces.ifaddresses("wlan0")[netifaces.AF_INET][0]['addr']
        return ip
    except:
        pass
    try:
        ip = netifaces.ifaddresses("eth0")[netifaces.AF_INET][0]['addr']
        return ip
    except:
        pass
    return None

def get_ssid():
    ret = subprocess.check_output(['iwconfig', 'wlan0']).split()
    ssid = [s.decode() for s in ret if s.startswith(b'ESSID')][0]
    return ssid

def is_PC_working():
    try:
        subprocess.check_output(['ping', '-c', '1', '-W', '1', slackbot_settings.PC_ADDR])
        return True
    except:
        return False

def is_PC_connectable():
    return send_receive('hello') == 'world'

def boot_PC():
    send_magic_packet(slackbot_settings.slackbot_settings.PC_MAC)

def wait_boot():
    timeout = 60
    for _ in range(timeout):
        if is_PC_working():
            return True
        time.sleep(1)
    return False

def wait_connect():
    timeout = 60
    for _ in range(timeout):
        if is_PC_connectable():
            return True
        time.sleep(1)
    return False

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        try:
            s.connect((slackbot_settings.PC_ADDR, slackbot_settings.PORT))
            s.sendall(message.encode())
        except:
            return True
    return False

def send_receive(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        try:
            s.connect((slackbot_settings.PC_ADDR, slackbot_settings.PORT))
            s.sendall(message.encode())
            data = s.recv(1024)
            return data.decode()
        except:
            return None

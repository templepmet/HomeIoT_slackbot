import slackbot_settings
import netutils
import fileutils
import subprocess

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slacker import Slacker

# メンション付きメッセージへの応答
# @respond_to('こんにちは')
# def greeting1(message):
#     message.reply('こんにちは')

@listen_to('^test$')
def test(message):
    message.send('test！')

@listen_to('^help$')
def help(message):
    res = ''
    res += 'status: ネットワーク接続情報\n'
    res += 'capture: 撮影した写真を送信\n'
    res += 'boot: PCを起動させる\n'
    res += 'reboot: PCを再起動させる\n'
    res += 'sleep: PCをスリープさせる\n'
    res += 'shutdown: PCをシャットダウンさせる\n'
    res += 'togglemute: PCのミュートを切替\n'
    res += 'volumeup: PCの音量を4上げる\n'
    res += 'volumedown: PCの音量を4下げる\n'
    res += 'togglesound: PCの音声ソースを切替\n'
    res += 'youtube: PCでYouTubeを再生\n'
    message.send(res)

@listen_to('^status$')
def status(message):
    ip = netutils.get_ip()
    ssid = netutils.get_ssid()

    res = ''
    if ssid is not None:
        res += ssid + '\n'
    res += 'ip: {}\n'.format(ip)

    res += 'TEMPLE-PC: '
    if netutils.is_PC_working():
        res += ':ok:\n'
    else:
        res += ':ng:\n'
    
    res += 'MyApp: '
    if netutils.is_PC_connectable():
        res += ':ok:\n'
    else:
        res += ':ng:\n'

    message.send(res)

@listen_to('^capture$')
def capture(message):
    slack = Slacker(slackbot_settings.API_TOKEN)
    channel = message.channel._body['name']
    filename = fileutils.capture()
    slack.files.upload(file_=filename, channels=channel)
    fileutils.remove(filename)

@listen_to('^boot$')
def boot(message):
    if netutils.is_PC_working():
        message.send('already working!')
        return
    netutils.boot_PC()
    message.send('send magic packet')
    if netutils.wait_boot():
        message.send('PC boot!')
    else:
        message.send('PC not boot...')
        return
    if netutils.wait_connect():
        message.send('MyApp connected!')
    else:
        message.send('MyApp not connected...')

@listen_to('^reboot$')
@listen_to('^sleep$')
@listen_to('^shutdown$')
@listen_to('^togglemute$')
@listen_to('^volumeup$')
@listen_to('^volumedown$')
@listen_to('^togglesound$')
def send(message):
    is_failed = netutils.send_message(message.body['text'])
    if is_failed:
        message.send('failed')
    else:
        message.send('send to pc')

@listen_to('^tv$')
def check_send(message):
    if not netutils.is_PC_working():
        boot(message)
    is_failed = netutils.send_message(message.body['text'])
    if is_failed:
        message.send('failed')
    else:
        message.send('send to pc')

@listen_to('^youtube(\s.+)?$')
def youtube(message, query):
    check_send(message)

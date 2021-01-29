import time
import pickle
import datetime

import paramiko
from flask import Flask
from flask import render_template

from config import SSH_HOST, SSH_PASS, SSH_USER


app = Flask(__name__, static_url_path='/static')


def prep_lv(lv):
    if lv[0] == '5':
        return "<span class='red'>5 STRONG SELL</span>"
    if lv[0] == '4':
        return "<span class='red'>4 SELL</span>"
    if lv[0] == '3':
        return "<span class='yellow'>3 HOLD</span>"
    if lv[0] == '2':
        return "<span class='green'>2 BUY</span>"
    if lv[0] == '1':
        return "<span class='green'>1 STRONG BUY</span>"


def get_todays_news():
    ret = []
    with open('symbols_new2.pickle', 'rb') as f:
        data = pickle.load(f)
    today = datetime.datetime.today().date()
    debugdt = datetime.date(year=2021, month=1, day=15)
    for (symbol, lv, dt) in data:
        if dt == "":
            continue
        if dt.date() != today and dt.date() != debugdt:
            continue
        ret.append((symbol, prep_lv(lv), dt.strftime('%d.%m.%Y')))
    return ret


def get_periodically():
    while True:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASS)
        _, ssh_stdout, ssh_stderr = ssh.exec_command('cd zacks && python3 util.py')
        print(ssh_stdout.readlines())
        print(ssh_stderr.readlines())

        sftp = ssh.open_sftp()
        sftp.get('symbols_new2.pickle', 'symbols_new2.pickle')
        sftp.close()
        ssh.close()
        time.sleep(60 * 60 * 12)


@app.route('/', methods=['GET'])
def index():
    data = get_todays_news()
    return render_template("index.html", data=data)


if __name__ == '__main__':
    # get_periodically()
    app.run(host='0.0.0.0', port=6001)

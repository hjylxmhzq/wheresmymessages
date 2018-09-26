from flask import Flask
import shutil, os, time
import itchat
from flask import render_template
import random

app = Flask(__name__)
id = random.randint(0,100000000)
usedid = []

@app.route('/')
def return_index():
    return render_template('index.html')

@app.route('/loading')
def return_loading():
    return render_template('loading.html')

first_run = 1

@app.route('/exit')
def kill_process():
    ps = os.popen('ps -l')
    pslist = []
    for i in ps:
        pslist.append(i.strip())
    if len(pslist)>1:
        for i in pslist[1:]:
            pid = i.split()[3]
            ppid = i.split()[4]
            print("pid:{}\nppid:{}".format(pid,ppid))
            if int(ppid)<1000:
                os.system('kill {}'.format(pid))
    os.system('ps -l')

@app.route('/login')
def return_qrcode():
    global usedid
    global id
    global first_run
    ps = os.popen('ps -l')
    pslist = []
    for i in ps:
        pslist.append(i.strip())
    if len(pslist)>1:
        for i in pslist[1:]:
            pid = i.split()[3]
            ppid = i.split()[4]
            print("pid:{}\nppid:{}".format(pid,ppid))
            if int(ppid)<1000:
                os.system('kill {}'.format(pid))
    os.system('ps -l')
    if os.path.exists('QR.png'):
        os.remove('QR.png')
    os.system('python3 test.py &')
    first_run = 0
    n=0
    while(not os.path.exists('QR.png')):
        n+=1
        if n==9:
            return """<p>登录失败，请刷新网页</p>"""
        time.sleep(1)
    shutil.copy('QR.png',os.getcwd()+"/static/QR_"+str(id)+".png")
    src = "/static/QR_"+str(id)+".png"
    if len(usedid)>50:
        flist = list(os.walk('./static'))
        for i in flist[0][2]:
            os.remove(flist[0][0]+'/'+i)
        usedid = []
    usedid.append(id)
    id = random.randint(0,100000000)
    while id in usedid:
        id = random.randint(0,100000000)
    return render_template('qrcode.html',source = src)


if __name__ == '__main__':
    app.run()
import argparse
import json
import multiprocessing
import re
import socket
import threading
import time
import os
from urllib import request
from flask import Flask, Response, request
import requests
import pymysql

tMap = {}
bMap = {}
app = Flask(__name__)


@app.route('/')
def init():
    msg = requests.get('http://localhost:' + str(request_dns() + "/index.html"), headers=request.headers,
                       data=request.data)
    return Response(msg)


@app.route('/index.html')
def init1():
    msg = requests.get('http://localhost:' + str(request_dns()) + "/index.html", headers=request.headers,
                       data=request.data)
    # print("=============================================================")
    # print('http://localhost:'+str(request_dns()))
    # print("=============================================================")
    return Response(msg)


@app.route('/swfobject.js')
def swf():
    msg = requests.get('http://localhost:' + str(request_dns() + "/swfobject.js"), headers=request.headers,
                       data=request.data)
    return Response(msg)


@app.route('/StrobeMediaPlayback.swf')
def smp():
    msg = requests.get('http://localhost:' + str(request_dns()) + "/StrobeMediaPlayback.swf", headers=request.headers,
                       data=request.data)
    return Response(msg)


def check_init(port):
    msg = requests.get('http://localhost:' + str(port) + "/vod/big_buck_bunny.f4m")
    brate_list = re.compile('bitrate="\d+"').findall(msg.text)
    bitRates = []
    for item in brate_list:
        bitRates.append(int(re.search('\d+', item).group()))
    lock.acquire()
    bMap[port] = sorted(bitRates)
    tMap[port] = bMap[port][0] * 1.5 + 0.0001
    lock.release()
    return msg


@app.route('/vod/<resource>')
def Vod(resource):
    port = request_dns()
    if resource == 'big_buck_bunny.f4m':
        msg = requests.get('http://localhost:' + str(port) + "/vod/big_buck_bunny_nolist.f4m")
        return Response(msg)
    else:
        all = re.findall(r'\d+', resource)
        seqNum = all[1]
        fragNum = all[2]
        if port not in tMap.keys():
            check_init(port)
        tC = tMap[port]
        bitrate = 10
        for item in bMap[port]:
            if 1.5 * item <= tC:
                bitrate = item
        ts = time.time()

        res = requests.get(
            'http://localhost:' + str(port) + '/vod/' + f'{bitrate}Seg{seqNum}-Frag{fragNum}',
            headers=request.headers, data=request.data)
        tf = time.time()
        duration = tf - ts
        length = int(res.headers.get('Content-Length'))
        tN = (length * 8 / 1024) / (tf - ts)
        # tN = (length * 8 /1024) / duration
        lock.acquire()
        tMap[port] = args.a * tN + (1 - args.a) * tC
        # logFile.write(f'{ts} {tf - ts} {tN} {tMap[port]} {bitrate} {port} {bitrate}Seg{seqNum}-Frag{fragNum}\n')
        logFile.write(f'{ts} {duration} {tN} {tMap[port]} {bitrate} {port} {bitrate}Seg{seqNum}-Frag{fragNum}\n')
        logFile.flush()
        lock.release()
        return Response(res)


def request_dns(message='port'):
    # return 8080
    serverName = '127.0.0.1'
    serverPort = 8888
    socketAddress = (serverName, serverPort)
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss.sendto(message.encode('utf-8'), socketAddress)
    msg, _ = ss.recvfrom(1024)
    if not msg:
        print("None recevied\n")
    return msg.decode('utf-8').strip()


def connectMysql():
    try:
        db = pymysql.connect(host='101.34.204.124',
                             user='user',
                             password='123456',
                             database='Danmuku')
        print('?????????????????????!')
        return db
    except pymysql.Error as e:
        print('?????????????????????' + str(e))


@app.route('/getDamuku/<lastTime>')
def getDanmuku(lastTime):
    print("sdfgsdherhdfh")
    cursor = db.cursor()
    lastTime = float(lastTime)
    sql = "select * from danmuku where time >= %s and time < %s;" % (lastTime, lastTime + 1)
    cursor.execute(sql)
    results = cursor.fetchall()

    json_list = []
    for res in results:
        result_json = {"id": res[0], "username": res[1], "item": res[2], "time": res[3]}
        json_list.append(result_json)
    msg = json.dumps(json_list)
    # print("result:",results )
    response: Response = Response(msg)
    response.access_control_allow_origin = '*'
    return response


@app.route('/post/', methods=['POST'])
def post():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        username = data['username']
        item = data['item']
        videoTime = data['time']
        cursor = db.cursor()
        sql = "insert into Danmuku.danmuku (username, item, time) values (%s, '%s', %s);" \
              % (username, item, videoTime)
        logFile.write(sql)
        logFile.flush()
        cursor.execute(sql)
        db.commit()
    response: Response = Response('')
    response.access_control_allow_origin = '*'
    return response


if __name__ == '__main__':
    db = connectMysql()
    lock = threading.Lock()
    getDanmuku(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, required=True)
    parser.add_argument("-a", "--a", type=float, required=True)
    args = parser.parse_args()
    filen = 'starter_proxy/logs/' + str(args.a) + args.filename
    # os.mknod(filen)
    global logFile
    logFile = open(filen, "w+")
    pro=multiprocessing.Process(target=app.run, kwargs=dict(port=8021))
    pro.start()
    while True:
        ifexit = input()
        if ifexit == 'exit':
            logFile.close()
            pro.terminate()
            db.close()
            exit(0)




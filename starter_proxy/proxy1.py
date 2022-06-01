import argparse
import json
import re
import socket
import time
import os
from urllib import request
from flask import Flask, Response,request
import requests
import pymysql

tMap={}
bMap={}
app = Flask(__name__)
@app.route('/')
def init():
        msg=requests.get('http://localhost:'+str(request_dns()+ "/index.html"),headers=request.headers,data=request.data)
        return Response(msg)
@app.route('/index.html')
def init1():
        msg=requests.get('http://localhost:'+str(request_dns()) + "/index.html" ,headers=request.headers,data=request.data)
        # print("=============================================================")
        # print('http://localhost:'+str(request_dns()))
        # print("=============================================================")
        return Response(msg)

@app.route('/swfobject.js')
def swf():
        msg=requests.get('http://localhost:'+str(request_dns()+"/swfobject.js"),headers=request.headers,data=request.data)
        return Response(msg)
@app.route('/StrobeMediaPlayback.swf')
def smp():
        msg=requests.get('http://localhost:'+str(request_dns())+"/StrobeMediaPlayback.swf",headers=request.headers,data=request.data)
        return Response(msg)
def check_init(port):
    msg = requests.get('http://localhost:' + str(port) + "/vod/big_buck_bunny.f4m")
    brate_list = re.compile('bitrate="\d+"').findall(msg.text)
    bitRates = []
    for item in brate_list:
        bitRates.append(int(re.search('\d+', item).group()))
    bMap[port] = sorted(bitRates)
    tMap[port] = bMap[port][0] * 1.5 + 0.0001
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
        bitrate=10
        for item in bMap[port]:
            if 1.5 * item <= tC:
                bitrate = item
        ts = time.time()
        
        res = requests.get(
            'http://localhost:' + str(port) + '/vod/' + f'{bitrate}Seg{seqNum}-Frag{fragNum}',
            headers=request.headers, data=request.data)
        tf = time.time()
        length = int(res.headers.get('Content-Length'))
        tN = (8*length / 1024) / (tf - ts)
        tMap[port] = args.a * tN + (1 - args.a) * tC
        logFile.write(f'{ts} {tf - ts} {tN} {tMap[port]} {bitrate} {port} {bitrate}Seg{seqNum}-Frag{fragNum}\n')
        logFile.flush()
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

def calculate_throughput():
    """
    Calculate throughput here.
    """

def connectMysql():
    try:
        db = pymysql.connect(host='127.0.0.1',
                     user='user',
                     password='123456',
                     database='Danmuku')

        print('数据库连接成功!')
        return db
    except pymysql.Error as e:
        print('数据库连接失败'+str(e))

@app.route('/getDamuku/<requestTime>/<lastTime>')
def getDanmuku(requestTime,lastTime):
    print("getDan" + requestTime)
    db.ping(reconnect=True)
    cursor = db.cursor()
    lastTime = float(lastTime)
    sql = "select * from danmuku where time >= %s and time < %s;" % (lastTime, lastTime+1)
    print(sql)
    cursor.execute(sql)
    # db.commit()  
    results = cursor.fetchall()

    json_list = []
    for res in results:
        result_json = {"id": res[0],"username": res[1],"item": res[2],"time": res[3]}
        json_list.append(result_json)
    msg = json.dumps(json_list)
    # print("result:",results )
    response: Response = Response(msg)
    response.access_control_allow_origin='*'
    return response

@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))  
        username =  data['username']
        item = data['item']
        videoTime = str(float(data['time']) + 2)
        cursor = db.cursor()
        sql = "insert into Danmuku.danmuku (username, item, time) values (%s, '%s', %s);" \
        % (username, item, videoTime)
        db.ping(reconnect=True)
        cursor.execute(sql) 
        db.commit()   
    response: Response = Response('')
    response.access_control_allow_origin='*'
    return response

@app.route('/comment', methods=['POST'])
def comment():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))  
        username =  data['username']
        item = data['item']
        videoTime = str(float(data['time']) + 2)
        cursor = db.cursor()
        sql = "insert into Danmuku.comment (username, item, time) values (%s, '%s', %s);" \
        % (username, item, videoTime)
        db.ping(reconnect=True)
        cursor.execute(sql) 
        db.commit()
    response: Response = Response('')
    response.access_control_allow_origin='*'
    return response

@app.route('/getComment/<requestTime>')
def getComment(requestTime):
    print("getComment" + requestTime)
    db.ping(reconnect=True)
    cursor = db.cursor()
    sql = "select * from Danmuku.comment;" 
    print(sql)
    cursor.execute(sql)
    # db.commit()  
    results = cursor.fetchall()

    json_list = []
    for res in results:
        result_json = {"id": res[0],"username": res[1],"item": res[2],"time": res[3]}
        json_list.append(result_json)
    msg = json.dumps(json_list)
    # print("result:",results )
    response: Response = Response(msg)
    response.access_control_allow_origin='*'
    return response


if __name__ == '__main__':
    db = connectMysql()
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, required=True)
    parser.add_argument("-a", "--a", type=float, required=True)
    args = parser.parse_args()
    filen='starter_proxy/logs/' + str(args.a) + args.filename
    # os.mknod(filen)
    global logFile
    logFile = open(filen, "w+")
    app.run(port=8999)
    db.close()

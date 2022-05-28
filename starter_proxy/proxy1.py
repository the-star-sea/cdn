import argparse
import re
import socket
import time
from urllib import request
from flask import Flask, Response,request
import requests
tMap={}
bMap={}
app = Flask(__name__)
a=0.5
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
        msg=check_init(port)
        return Response(msg)
    else:
        all = re.findall(r'\d+', resource)
        seqNum = all[1]
        fragNum = all[2]
        if port not in tMap.keys():
            check_init(port)
        tC = tMap[port]
        bitrate=-1000
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
        tMap[port] = a * tN + (1 - a) * tC
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

def init_log_file():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, required=True)
    args = parser.parse_args()
    global logFile 
    logFile= open('logs/'+args.filename,"w")

if __name__ == '__main__':
    init_log_file()
    app.run(port=8999)

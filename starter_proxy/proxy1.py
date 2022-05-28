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
@app.route('/vod/<resource>')
def Vod(resource):
    port = request_dns()
    if port not in tMap.keys():
        msg = requests.get('http://localhost:' + str(port) + "/vod/big_buck_bunny.f4m")
        brate_list = re.compile('bitrate="\d+"').findall(msg.text)
        bitRates = []
        for item in brate_list:
            bitRates.append(int(re.search('\d+', item).group()))
        bMap[port] = sorted(bitRates)
        tMap[port] = bMap[port][0]
    if resource == 'big_buck_bunny.f4m':
        return Response(msg)
    else:
        all = re.findall(r'\d+', resource)
        seqNum = all[1]
        fragNum = all[2]
        tC = tMap[port]
        for item in bMap[port]:
            if 1.5 * item <= tC:
                bitrate = item
        ts = time.time()
        serverResponse = requests.get(
            'http://localhost:' + str(port) + '/vod/' + f'/vod/{bitrate}Seg{seqNum}-Frag{fragNum}',
            headers=request.headers, data=request.data)
        tf = time.time()
        length = int(serverResponse.headers.get('Content-Length'))
        tN = length / (tf - ts)
        tMap[port] = a * tN + (1 - a) * tC
        return Response(serverResponse)




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
    # print(bytes.decode(msg[0]),flush=True)
    return msg.decode('utf-8').strip()

def calculate_throughput():
    """
    Calculate throughput here.
    """


if __name__ == '__main__':
    app.run(port=8999)

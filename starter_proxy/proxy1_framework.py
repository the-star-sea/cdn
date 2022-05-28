import socket
from urllib import request
from flask import Flask, Response,request
import requests
bitRatesMap={}
app = Flask(__name__)

@app.route('/')
def init():
        msg=requests.get('http://localhost:'+str(request_dns()),headers=request.headers,data=request.data)
        return Response(msg)
@app.route('/index.html')
def init1():
        msg=requests.get('http://localhost:'+str(request_dns()) + "/index.html" ,headers=request.headers,data=request.data)
        print("=============================================================")
        print('http://localhost:'+str(request_dns()))
        print("=============================================================")
        return Response(msg)

@app.route('/swfobject.js')
def swf():
        msg=requests.get('http://localhost:'+str(request_dns()+"/swfobject.js"),headers=request.headers,data=request.data)
        return Response(msg)
@app.route('/StrobeMediaPlayback.swf')
def smp():
        msg=requests.get('http://localhost:'+str(request_dns())+"/StrobeMediaPlayback.swf",headers=request.headers,data=request.data)
        return Response(msg)
@app.route("/vod/<resource>")
def Vod(resource):
    if resource == 'big_buck_bunny.f4m':
        port=request_dns()
        msg=requests.get('http://localhost:'+str(port)+"/vod/big_buck_bunny.f4m")
        return Response(msg)
    else:
        port=request_dns()
        print(resource)
        serverResponse=requests.get('http://localhost:'+str(port)+'/vod/1000'+resource,headers=request.headers,data=request.data)
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

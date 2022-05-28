import argparse
import socket

class DNSServer:
    def __init__(self, ip, port, servers) -> None:
        self.ip = ip
        self.port = port
        self.servers = []
        self.read_server_ports(servers)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
    
    def start(self):
        while True:
            message, address = self.receive()
            message = message.decode('utf-8')
            print("receive: %s" % message)
            self.replay(message, address)  
        
    def receive(self):
        return self.socket.recvfrom(8192)
    
    def replay(self, response, address):
        self.socket.sendto(str(self.servers[0]).encode('utf-8'), address)
        
    def read_server_ports(self, servers):
        with open(servers, 'r') as f:
            port_lines = f.readlines()
            self.servers = [int(port) for port in port_lines]

def get_agrgument():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="")
    parser.add_argument("--port", type=int, default="8888")
    parser.add_argument("--servers",type=str, required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_agrgument()
    dns_server = DNSServer(args.ip, args.port, args.servers)
    dns_server.start()
    
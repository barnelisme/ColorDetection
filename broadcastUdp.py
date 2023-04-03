import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

Port=22222

def Broadcast(msg):
    message=bytes(msg,'utf-8')
    server.sndto(message,('<broadcast>',Port))
    
    
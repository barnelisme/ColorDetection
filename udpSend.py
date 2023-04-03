import socket

UDP_IP_ADDRESS = "192.168.0.118"  #"172.20.10.3" #"192.168.189.119"  #"127.0.0.1"  
UDP_PORT_NO = 22222 #33446 
message = "0"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Sending Signal to a specific IP Address
def setMessage(msg):
    message = msg
    try :
        clientSocket.sendto(bytes(message, 'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    except :
        clientSocket.sendto(bytes(message, 'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
        # print("none exist")
    pass

#Broadcasting Signal to all IP Addresses
def broadcastMessage(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # print("Broadcasting")
        
    sock.sendto(bytes(msg, "utf-8"), ("255.255.255.255", 22222))
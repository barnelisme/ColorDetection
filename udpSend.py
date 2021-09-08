import socket

UDP_IP_ADDRESS = "192.168.8.128"
UDP_PORT_NO = 22222
message = "0"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def setMessage(msg):
    message = msg
    try:
        clientSocket.sendto(bytes(message, 'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    except:
        clientSocket.sendto(bytes(message, 'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
        # print("none exist")
    pass


import socket
#import RPi.GPIO as GPIO

# Recive data from client and decide which function to call


message_received = " "
def Receive():
#while True:
    # Create a Server Socket and wait for a client to connect
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 55552))
    # End Of Serever Socket Creation

    dataFromClient, address = server_socket.recvfrom(256)
    tempString = str(dataFromClient)

    if "Calibration" in tempString:
        message_received = "Calibration"
        # trackColor.checkMessage = 1;

    elif "Reset" in tempString:
        message_received = "Reset"
        # trackColor.checkMessage = 0;

    elif "Simulate" in tempString:
        message_received = "Simulate"
        # trackColor.checkMessage = 0;
    else:
        message_received = "NONE"

    # options[dataFromClient]()
    # print(message_received)
    return str(message_received)

    #print(message_received)
    #break

def ReceiveV2(sock):
#while True:
    try:
        # Create a Server Socket and wait for a client to connect
        
        # End Of Serever Socket Creation

        dataFromClient, address = sock.recvfrom(256)
        tempString = str(dataFromClient)


        if "Calibration" in tempString:
            message_received = "Calibration"
            # trackColor.checkMessage = 1;

        elif "Reset" in tempString:
            message_received = "Reset"
            # trackColor.checkMessage = 0;

        elif "Simulate" in tempString:
            message_received = "Simulate"
            # trackColor.checkMessage = 0;
            
        else:
            message_received = tempString

        # options[dataFromClient]()
        # print(message_received)
        return str(message_received)
    
    except Exception as e:
        #print("ERROR:", e)
        return "NONE"
        pass

    

    #print(message_received)
    #break


    '''
    import socket
#import RPi.GPIO as GPIO


# Create a Server Socket and wait for a client to connect
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 55554))
#print ("UDPServer Waiting for client on port 55554")


# Recive data from client and decide which function to call
def receiveData():

    if not server_socket.recvfrom(1125):
        print("empty")

    else:
        #print("Occupied")
        dataFromClient, address = server_socket.recvfrom(256)
        tempString = str(dataFromClient)


    if "Calibration" in tempString:
        message_received = "Calibration"
        # trackColor.checkMessage = 1;

    if "Stop" in tempString:
        message_received = "Stop"
        # trackColor.checkMessage = 0;
    # options[dataFromClient]()

    print(message_received)
    #break
    '''
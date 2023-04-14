import socket
import threading
import time
#
UDP_IP1 = socket.gethostname()
UDP_PORT1 = 48901
UDP_IP2 = socket.gethostname()
UDP_PORT2 = 48902
#
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.bind((UDP_IP1, UDP_PORT1))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.bind((UDP_IP2, UDP_PORT2))
#
#
# def monitor_socket(name, sock):
#     while True:
#         sock1.recv is not None:
#         data, addr = sock.recvfrom(1024)
#         data_int = int(data)
#         print(name, data_int)
# #
# #
# # t1 = threading.Thread(target=monitor_socket, args=["SensorTag[1] RSSI:", sock1
# # t1.daemon = True
# # t1.start()
# #
# # t2 = threading.Thread(target=monitor_socket, args=["SensorTag[2] RSSI:", sock2])
# # t2.daemon = True
# # t2.start()
#
# while True:
#     if sock1.recv is not None:
#         data1, addr = sock1.recvfrom(1024)
#         data1_int = int(data1)
#         print
#         "SensorTag[1] RSSI:", data1_int
#     #  We don't want to while 1 the entire time we're waiting on other threads
#     time.sleep(1)


import time

# Define a function for the thread
def print_time(name ):
   delay = 2
   count = 0
   while True:
      #time.sleep(delay)
      count += 1
      print ("%s: %s" % ( name, time.ctime(time.time()) ))
      if sock1.recv is not None:
        data1, addr = sock1.recvfrom(1024)

        print("SensorTag[1] RSSIsTR:", str(data1))

# Create two threads as follows
try:
   thread1 = threading.Thread(target = print_time("Kam"))
   thread1.start()

except Exception as err:
   print ("Error: unable to start thread" + err)

while 1:
   pass
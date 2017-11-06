import serial
import socket
from time import sleep


ser = serial.Serial('dev/ttyUSB0',115200,timeout=5)
sleep(2)

soc = socket.socket()
host = "192.168.1.136"
port = 1990
soc.bind((host,port))
soc.listen(1)

while(True):
    print("Online")
    conn,addr = soc.accept()
    print("Connected")
    while(True):
        data = conn.recv(512)
        data = data.rstrip()
        if not data:
            conn.close()
            print("Disconnected")
            sendData(90,60)
            break

        data = data.decode("utf-8")
        datalist = data.split(",")
        x = datalist[0]
        y = datalist[1]
        sendData(x, y)


def sendData(x, y):
    send = x+";"+y+"\r\n"
    send = sendData.encode()
    ser.write(send)
    print("X: ",x,"Y: ",y)

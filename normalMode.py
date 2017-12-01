
import serial
import socket

from time import sleep


def neww():
    soc = socket.socket()
    host = "192.168.1.169"
    port = 1990
    soc.bind((host,port))
    soc.listen(1)
    while(True):
        print("Online")
        conn,addr = soc.accept()
        print("Connected")
        while(True):
            data = conn.recv(32)
            if not data:
                conn.close()
                print("Disconnected")
                break
            data = data.rstrip()
            data = data.decode("utf-8")
            #print(data)
            datalist = data.split(",")
            x = datalist[0]
            y = datalist[1]
            Fdata = str(x) + ";" + str(y)
            #Fdata = x+";"+y+"\r\n"
            print(Fdata)
            Fdata = Fdata.encode()
            ser.write(Fdata)

ser = serial.Serial('COM3',115200,timeout=5)

neww()

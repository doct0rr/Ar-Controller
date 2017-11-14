
import serial
import socket
import threading
from queue import Queue
from time import sleep
from threading import Event

dataPoints = Queue()
event = Event()


def mapper(x, inMin, inMax, outMin, outMax):
    return ((x - inMin) * (outMax - outMin))/ ((inMax - inMin) + outMin)


def dataFromSocket(inQ):
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
            data = conn.recv(32)
            if not data:
                conn.close()
                print("Disconnected")
                break
            data = data.rstrip()
            data = data.decode("utf-8")
            #print(data)
            inQ.put(data)
            event.set()


def getDataFromQueue(outQ):
    event.wait()
    if not outQ.empty() :
        data = outQ.get()
        datalist = data.split(",")
        x = datalist[0]
        y = datalist[1]
        if x!= "null" and y !="null":
            try:
                x = float(x)
                y = float(y)
                event.clear()
                return (x, y)
            except:
                return (x,y)
        else:
            return(90, 60)
    else:
        event.clear()
        return (90, 60)

def panValues(defaultPan, x):
    left  = defaultPan - 156
    right = defaultPan + 156
    newX  = x
    if right > 313 and x < 0:
        newX = 626 + x
    finalX = mapper(newX, left, right, 0, 180)
    finalX = int(finalX)
    return finalX


def loop():
    while True:
        for i in range(100):
            x,y = (getDataFromQueue(dataPoints))
            defaultPan  = x
            print("default is ",x)
        while (True):
            x,y = (getDataFromQueue(dataPoints))
            #print("X: ",x,"Y: ",y)
            if(isinstance(x,str) and isinstance(y,str)):
                continue
            if(not dataPoints.empty()):
                break
            mappedX = panValues(defaultPan, x)
            print("mappedX: ",mappedX,"X: ",x,"Y: ",y)
            finalSend = str(mappedX) + ";" + str(y) + "\r\n"
            finalSend=finalSend.encode()
            ser.write(finalSend)


if __name__ == '__main__':
    t1 = threading.Thread(target = dataFromSocket, args = (dataPoints, ))
    t2 = threading.Thread(target = loop)
    ser = serial.Serial('/dev/ttyUSB0',115200,timeout=5)
    t2.start()
    t1.start()

import serial
import socket
import threading
from queue import Queue
from time import sleep
from threading import Event

dataPoints = Queue()
event = Event()

#ser = serial.Serial('dev/ttyUSB0',115200,timeout=5)
sleep(2)
defaultSample = 400

def dataFromSocket(inQ):
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
            data = conn.recv(512)
            if not data:
                conn.close()
                print("Disconnected")
                break
            data = data.rstrip()
            data = data.decode("utf-8")
            print(data)
            inQ.put(data)
            event.set()




def mapper(x, inMin, inMax, outMin, outMax):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def panValues(defaultPan, x):
    left  = defaultPan - 156
    right = defaultPna + 156
    newX  = x
    if right > 313 and x < 0:
        newX = 626 + x
    finalX = mapper(newX, left, right, 0, 180)
    return finalX


def tiltValue():
    return False


def getDataFromQueue(outQ):
    event.wait()
    if container.acquire(True) and not outQ.empty() :
        data = outQ.get()
        datalist = data.split(",")
        x = datalist[0]
        y = datalist[1]
        event.clear()
        return x, y
    else:
        event.clear()
        return (90, 60)


def loop():
    while True:
        print(getDataFromQueue(dataPoints))


def worker():
    for i in range(defaultSample):
        x,y    = getDataFromQueue(dataPoints)
        defaultPan  = x
        defaultTilt = y
    while True:
        x,y = getDataFromQueue(dataPoints)




def sendData(x, y):
    send = x+";"+y+"\r\n"
    send = sendData.encode()
    ser.write(send)
    #print("X: ",x,"Y: ",y)


if __name__ == '__main__':
    t1 = threading.Thread(target = dataFromSocket, args = (dataPoints, ))
    t2 = threading.Thread(target = loop)

    t1.start()
    sleep(5)
    t2.start()

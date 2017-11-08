import serial
import socket
import threading
from queue import Queue
from time import sleep
from threading import Event

dataPoints = Queue()
event = Event()
defaultPanFlag = False
#ser = serial.Serial('dev/ttyUSB0',115200,timeout=5)
sleep(2)
defaultSample = 100

def dataFromSocket(inQ):
    global defaultPanFlag
    soc = socket.socket()
    host = "192.168.1.169"
    port = 1990
    soc.bind((host,port))
    soc.listen(1)
    while(True):
        print("Online")
        defaultPanFlag = True
        conn,addr = soc.accept()
        print("Connected")
        while(True):
            data = conn.recv(512)
            if not data:
                conn.close()
                print("Disconnected")
                defaultPanFlag = True
                break
            data = data.rstrip()
            data = data.decode("utf-8")
            #print(data)
            inQ.put(data)
            event.set()




def mapper(x, inMin, inMax, outMin, outMax):
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin


def panValues(defaultPan, x):
    left  = defaultPan - 156
    right = defaultPan + 156
    newX  = x
    if right > 313 and x < 0:
        newX = 626 + x
    finalX = mapper(newX, left, right, 0, 180)
    return finalX


def tiltValue():
    return False


def getDataFromQueue(outQ):
    event.wait()
    if not outQ.empty() :
        data = outQ.get()
        datalist = data.split(",")
        x = datalist[0]
        y = datalist[1].split("\n")
        y = y[0]
        if x!= "null" and y !="null":
            try:
                x = float(x)
                y = float(y)
                event.clear()
                return (x, y)
            except:
                return (90, 60)
        else:
            return(90, 60)
    else:
        event.clear()
        return (90, 60)

def getDefaultPan():
        for i in range(100):
            x,y = (getDataFromQueue(dataPoints))
            defaultPan  = x
        return defaultPan
def loop():
    global defaultPanFlag
    defaultPan = getDefaultPan()
    print(defaultPan)
    while True:
        if defaultPanFlag:
            defaultPan = getDefaultPan()
            print(defaultPan)
        x,y = (getDataFromQueue(dataPoints))
        mappedX = panValues(defaultPan,x)
        print("mappedX: ",mappedX,"X: ",x,"Y: ",y)
        defaultPanFlag = False


def worker():
    print("ok ?")
    for i in range(defaultSample):
        x,y    = getDataFromQueue(dataPoints)
        defaultPan  = x
        defaultTilt = y
    while True:
        print("HERE")
        x,y = getDataFromQueue(dataPoints)
        mappedX = panValues(defaultPan,x)
        print(mappedX,y)



def sendData(x, y):
    send = x+";"+y+"\r\n"
    send = sendData.encode()
    ser.write(send)
    #print("X: ",x,"Y: ",y)


if __name__ == '__main__':
    t1 = threading.Thread(target = dataFromSocket, args = (dataPoints, ))
    t2 = threading.Thread(target = loop)

    t2.start()
    t1.start()

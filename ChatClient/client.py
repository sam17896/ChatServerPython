import threading
import time
import socket

tLock = threading.Lock()
shutdown = False


def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print(str(data))
        except:
            pass
        finally:
            tLock.release()


host = '127.0.0.1'
port = 0

server = ('127.0.0.1', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("recvThread", s))
rT.start()

alias = input('Name: ')
message = input(alias+": ")

while message != 'q':
    if message != '':
        sendmessage = alias + ": " + message
        s.sendto(sendmessage.encode('UTF-8'), server)
    tLock.acquire()
    message = input(alias + ": ")
    tLock.release()
    time.sleep(0.2)

shutdown = True
rT.join()
s.close()

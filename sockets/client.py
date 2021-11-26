# python client.py
import socket
import threading


def listen():
    while True:
        mess = clientsocket.recv(1024)
        print(mess.decode("utf-8"))


host = 'localhost'
port = 5555

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.connect((host, port))
thread = threading.Thread(target=listen)
thread.start()


while True:
    mess = input()
    if mess == '':
        break
    clientsocket.sendto(('Your friend: ' + mess).encode('utf-8'), (host, port))
clientsocket.close()

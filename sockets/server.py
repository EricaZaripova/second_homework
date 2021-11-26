# python server.py
import socket


host = 'localhost'
port = 5555

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.bind((host, port))
print('Running...')

friends = {}


while True:
    mess, address = serversocket.recvfrom(1024)
    if address not in friends and len(friends) <= 100:
        print(f'New connection: {address[1]}')
        serversocket.sendto(f'Your room number {len(friends) // 2 + 1}'.encode('utf-8'), address)
        friends[address] = address
        for c1, c2 in friends.items():
            if c1 != address and c1 == c2:
                friends[c1] = address
                friends[address] = c1
                break
    if len(friends) <= 100:
        if friends[address] == address:
            mess = 'Friend not found yet'.encode('utf-8')
        serversocket.sendto(mess, friends[address])
    else:
        serversocket.sendto('Ooooooops! All the rooms are already occupied...'.encode('utf-8'), address)

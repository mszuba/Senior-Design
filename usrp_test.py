import socket

# set up server side (run first)

host = '192.168.10.1'
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',port))
BUFFER_SIZE = 1472
#s.setblocking(0)

print('Rx data...')
while True:
    n=0
    data = s.recv(BUFFER_SIZE)
    while n < BUFFER_SIZE:
        print(data[n])
        n+=1
    break #for testing
#conn.close()
s.close()

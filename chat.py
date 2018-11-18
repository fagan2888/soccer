import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('0.0.0.0', 10000))

sock.listen(1)

connections = []

def handler(c, a):
    while True:
        data = c.recv(1024)
        #sending back data to user
        for connection in connections:
            connection.send(bytes(data))
        if not data:
            connections.remove(c)
            c.close()
            break


while True:
    #c is connection
    #a is client's address
    c, a = sock.accept()
    cThread = threading.Thread(target = handler, args = (c, a))
    cThread.daemon = True
    cThread.start()
    connections.append(c)
    print(connections)

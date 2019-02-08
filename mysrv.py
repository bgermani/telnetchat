import socket
import threading


server = socket.socket()
server.bind(('', 4000))
server.listen(4)
clients = []
lock = threading.Lock()


class mainChat(threading.Thread):
    def __init__(self, (socket, address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address

    def broadcast(self, args):
        for client in clients:
            client.socket.send(args)

    def add_client(self):
        lock.acquire()
        self.socket.send('Type something and hit enter to send. "quit" disconnects.\n')
        self.broadcast(str(self.address) + " has joined the chat.\n")
        clients.append(self)
        lock.release()

    def remove_client(self):
        lock.acquire()
        clients.remove(self)
        lock.release()

    def interpreter(self, data):
        if str(data).rstrip() == 'quit':
            self.broadcast(str(self.address) + ' has left the chat.\n')
            self.socket.close()
            self.remove_client()
            return
        self.broadcast(str(self.address) + ' sends: "' + str(data).rstrip() + '"\n')

    def run(self):
        self.add_client()
        while 1:
            data = self.socket.recv(256)
            self.interpreter(data)
        self.socket.close()
        self.remove_client()


while 1:
    mainChat(server.accept()).start()

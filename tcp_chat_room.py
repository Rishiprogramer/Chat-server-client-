import threading
import socket

host = "YOUR LOCAL SERVER IP ADDRESS"
port = 5412

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)

        except ConnectionError:

            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} has been disconnected".encode('ascii'))
            break


def receive_clients():
    while True:
        client, address = server.accept()
        print("Connected with", address)

        client.send("nickname".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)
        print("Nickname of the client is", nickname)
        broadcast(f"{nickname} joined the chat".encode('ascii'))

        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive_clients()

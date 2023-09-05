import threading
import socket
from datetime import time

host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 5412

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()
print(f"Started listening at ip address {ip} and port {port}")
clients = []
nicknames = []


def broadcast(message, sender_client):
    for client in clients:
        try:
            client.send(message.encode('UTF-16'))
        except Exception as e:
            print(f"Error sending message to {client}: {e}")


def handle(client):
    while True:
        try:
            message = client.recv(4096).decode("UTF-16")
            if not message:
                break
            broadcast(message, client)

        except ConnectionError:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} has been disconnected", client)
            break


def receive_clients():
    while True:
        client, address = server.accept()
        print("Connected with", address)
        try:
            client.send("nickname".encode('UTF-16'))
            nickname = client.recv(1024).decode('UTF-16')

            nicknames.append(nickname)
            clients.append(client)
            print("Nickname of the client is", nickname)
            broadcast(f"{nickname} joined the chat \n", client)
            client.send("Connected to the server \n".encode('UTF-16'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except Exception as e:
            client.close()


receive_thread = threading.Thread(target=receive_clients)
receive_thread.start()


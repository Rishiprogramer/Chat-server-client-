import os
import threading
import socket
from datetime import time
import time

file_han = False
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 5412
#main server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()
#send_file_server
serverss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverss.bind((ip, 9850))
serverss.listen()
#uploadding
servers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servers.bind((ip, 9851))
servers.listen()

print(f"Started listening at ip address {ip} and port {port}")
clients = []
nicknames = []
file_don = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('UTF-16'))
        except Exception as e:
            print(f"Error sending message to {client}: {e}")


def file_Downloading():
    clientf, address = servers.accept()

    file_name = clientf.recv(1024).decode()
    print(f"Receiving file: {file_name}")

    # Receive the file size as a string
    file_size_str = clientf.recv(1024).decode()
    file_size = int(file_size_str)
    print(f"File size: {file_size} bytes")

    # Create/Open the file for writing in binary mode
    with open(file_name, "wb") as file:
        bytes_received = 0
        while bytes_received < file_size:
            # Determine the chunk size to receive
            chunk_size = min(file_size // 2, file_size - bytes_received)

            # Receive a chunk of data
            data = clientf.recv(chunk_size)

            if not data:
                break

            # Write the received data to the file
            file.write(data)
            bytes_received += len(data)

        print(f"Received {bytes_received} bytes")

    # Notify clients about the successful file transfer
    broadcast(f"Server: File uploaded named: {file_name}")
    servers.close()
    file_don.append(file_name)


def file_send(messagee):
    clientu, address = serverss.accept()
    message, don, name = messagee.split('|')
    path = name
    names = os.path.basename(path)

    file_size = os.path.getsize(path)

    print(f"File Size: {file_size} bytes")

    if file_size <= 1073741824000:
        clientu.send(names.encode())
        time.sleep(0.1)
        clientu.send(str(file_size).encode())

        with open(path, "rb") as file:
            data = file.read()
            clientu.sendall(data)

        time.sleep(0.2)


def handle(client):
    while True:
        try:
            message = client.recv(1048576).decode("UTF-16")
            if not message:
                break
            elif "!@#$%^&*()_+[][][][]?/<>?:12345678995841265vcxzsdfgbnumb" == message:
                donw = threading.Thread(target=file_Downloading)
                donw.start()
            elif "M#yP@4sS#w0rD1&L0nG*E9n0uGhT0P3rs!st" in message:
                print("ok")
                up = threading.Thread(target=file_send, args=(message,))
                up.start()

            else:

                broadcast(message)

        except ConnectionError:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} has been disconnected")
            break


def receive_clients():
    while True:
        client, address = server.accept()
        print("Connected with", address)
        try:
            client.send("789456123/*-+214785wesdftgb".encode('UTF-16'))
            nickname = client.recv(1048576).decode('UTF-16')

            nicknames.append(nickname)
            clients.append(client)
            #if len(file_don) > 0:
               #` client.send(f"addfilessppqqocode1123edskew: {file_don}")
            print("Nickname of the client is", nickname)
            broadcast(f"{nickname} joined the chat \n")
            client.send("Connected to the server \n".encode('UTF-16'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except Exception as e:
            client.close()


receive_thread = threading.Thread(target=receive_clients)
receive_thread.start()



import socket
import threading



nickname = input("Enter your nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('YOUR LOCAL SERVER IP ADDRESS', 5412))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'nickname':
                client.send(nickname.encode('ascii'))
            else:
                print(message)

        except:
            print("Error occurred")
            client.close()
            break


def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

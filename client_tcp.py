import os
import socket
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import *
from tkinter import *

# Initialize Tkinter
root = tk.Tk()
root.title("Chat App")
root.geometry("600x400")
nickname = socket.gethostname()

# Create a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.3', 5412)  # Replace with your server address and port
send_files = False
contacts = []

try:
    client.connect(server_address)
    print(f"Connected to {server_address[0]}:{server_address[1]}")

    # Create a GUI window
    chat_frame = tk.Frame(root)
    chat_frame.pack(fill="both", expand=True)

    # Create a contacts panal


    # Create a scrollbar
    scrollbar = tk.Scrollbar(chat_frame)
    scrollbar.pack(side="right", fill="y", padx=5)

    # Create a Text widget to display messages
    message_text = tk.Text(chat_frame, wrap="word", yscrollcommand=scrollbar.set, width=80, height=20)
    message_text.pack(side="left", fill="both", expand=True)
    message_text.config(state="disabled")  # Disable text widget to prevent editing

    # Link the scrollbar to the Text widget
    scrollbar.config(command=message_text.yview)

    # Get a list of all contacts
    contacts = []
    received_files = []


    def receive():
        while True:
            try:
                message = client.recv(1048576).decode('utf-16')
                if not message:
                    print("Server closed the connection.")
                    client.close()
                    break
                if message == '789456123/*-+214785wesdftgb':
                    client.send(nickname.encode('utf-16'))
                elif "Server: File uploaded named:" in message:
                    message_text.config(state="normal")
                    message_text.insert("end", message + "\n")
                    message_text.config(state="disabled")
                    message_text.see("end")
                    name = message.replace('Server: File uploaded named:', '')
                    received_files.append(name.strip())  # Add the received file name to the list
                    update_dropdown()

                else:
                    message_text.config(state="normal")
                    message_text.insert("end", message)
                    message_text.config(state="disabled")
                    message_text.see("end")  # Scroll to the end
            except Exception as e:
                print(f"Error occurred: {e}")
                client.close()
                break
    def send_message():
        global send_files
        if not send_files:
            message = message_entry.get()
            if message:
                formatted_message = f"{nickname}: {message}\n"
                client.send(formatted_message.encode('utf-16'))
                message_entry.delete(0, 'end')

    def send_messages(event):
        if event.keysym == 'Return' or event.keysym == 'enter':
            send_message()


    def send_file():
        global send_files
        try:
            path = filedialog.askopenfilename()
            if not path or path == '':
                return  # User canceled file selection
        except Exception as e:
            return


        def file_transfer_thread():
            client.send("!@#$%^&*()_+[][][][]?/<>?:12345678995841265vcxzsdfgbnumb".encode('utf-16'))
            global send_files

        # Create a separate socket for file transfer
            file_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            file_transfer_socket.connect(('192.168.1.4', 9851))

            try:
                name = os.path.basename(path)
                file_size = os.path.getsize(path)
                print(f"File Size: {file_size} bytes")

                if file_size <= 1073741824000:
                # send_files = True
                    file_transfer_socket.send(name.encode())
                    time.sleep(0.1)
                    file_transfer_socket.send(str(file_size).encode())

                    with open(path, "rb") as file:
                        data = file.read()
                        file_transfer_socket.sendall(data)

                    time.sleep(0.2)
                else:
                    messagebox.showwarning("File transfer is limited to 65 MB", "Limit crossed")
            except Exception as e:
                messagebox.showerror("File Transfer Error", str(e))
            finally:
                # Re-enable the send file button after transferring
                send_files_button.config(state="normal")

            # Close the file transfer socket
                file_transfer_socket.close()


    # Start the file transfer in a separate thread
        threading.Thread(target=file_transfer_thread).start()


    def update_dropdown():
        menu_var.set("")  # Clear the current selection
        menu["menu"].delete(0, "end")  # Clear the current menu items

        for name in received_files:
            menu["menu"].add_command(label=name, command=lambda n=name: send_download_request(n))


    def send_download_request(file_name):
        client.send(f"M#yP@4sS#w0rD1&L0nG*E9n0uGhT0P3rs!st|Download|{file_name}".encode('utf-16'))

        def download_file():
            down_file = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            down_file.connect(('192.168.1.4', 9850))
            print("iniciated")

            # Receive the file name
            file_name = down_file.recv(1024).decode()
            print(f"Receiving file: {file_name}")

            # Receive the file size as a string
            file_size_str = down_file.recv(1024).decode()
            file_size = int(file_size_str)
            print(f"File size: {file_size} bytes")

            # Create/Open the file for writing in binary mode
            with open(file_name, "wb") as file:
                bytes_received = 0
                while bytes_received < file_size:
                    # Determine the chunk size to receive
                    chunk_size = min(file_size // 2, file_size - bytes_received)

                    # Receive a chunk of data
                    data = down_file.recv(chunk_size)

                    if not data:
                        break

                    # Write the received data to the file
                    file.write(data)
                    bytes_received += len(data)

                send_files_button.config(state=NORMAL)
                send_button.config(state=NORMAL)
                print(f"Received {bytes_received} bytes")
                message_text.config(state="normal")
                message_text.insert("end", "File downloaded")
                message_text.config(state="disabled")
                message_text.see("end")

        # Start the download thread
        download_thread = threading.Thread(target=download_file)
        download_thread.start()


    # Create GUI elements
    message_entry = tk.Entry(root, width=80)
    message_entry.pack(fill="x", padx=10, pady=10)
    message_entry.bind("<Return>", send_messages)

    send_button = tk.Button(root, text="Send message", command=send_message)
    send_button.pack(anchor="center", padx=10, pady=10)

    send_files_button = tk.Button(root, text="Send file", command=send_file)
    send_files_button.pack(anchor="center", padx=15, pady=10)

    # Create a dropdown menu
    menu_var = tk.StringVar()
    menu_var.set("Select File to Download")  # Default message for the dropdown
    menu = tk.OptionMenu(root, menu_var, "Select File to Download")
    menu.pack(anchor="w", padx=10, pady=5)



    def download_selected_file():
        selected_file = menu_var.get()
        if selected_file != "Select File to Download":
            send_download_request(selected_file)

    # Start the receive thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
except Exception as e:
    print(e)
    messagebox.showerror("error", "Server is not running")


root.mainloop()


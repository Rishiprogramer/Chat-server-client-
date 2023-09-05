import os
import socket
import threading
import tkinter as tk
from tkinter import filedialog

# Initialize Tkinter
root = tk.Tk()
root.title("Chat App")
root.geometry("600x400")
nickname = input("Enter your nickname: ")
# Create a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.4', 5412)  # Replace with your server address and port

try:
    client.connect(server_address)
    print(f"Connected to {server_address[0]}:{server_address[1]}")

    # Create a GUI window
    chat_frame = tk.Frame(root)
    chat_frame.pack(fill="both", expand=True)

    # Create a scrollbar
    scrollbar = tk.Scrollbar(chat_frame)
    scrollbar.pack(side="right", fill="y", padx=5)

    # Create a Text widget to display messages
    message_text = tk.Text(chat_frame, wrap="word", yscrollcommand=scrollbar.set, width=80, height=20)
    message_text.pack(side="left", fill="both", expand=True)
    message_text.config(state="disabled")  # Disable text widget to prevent editing

    # Link the scrollbar to the Text widget
    scrollbar.config(command=message_text.yview)

    def receive():
        while True:
            try:
                message = client.recv(4096).decode('utf-16')
                if not message:
                    print("Server closed the connection.")
                    client.close()
                    break
                if message == 'nickname':
                    client.send(nickname.encode('utf-16'))
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
        message = message_entry.get()
        if message:
            formatted_message = f"{nickname}: {message}\n"
            client.send(formatted_message.encode('utf-16'))
            message_entry.delete(0, 'end')

    def send_messages(event):
        if event.keysym == 'Return' or event.keysym == 'enter':
            send_message()

    # Create GUI elements
    message_entry = tk.Entry(root, width=80)
    message_entry.pack(fill="x", padx=10, pady=10)
    message_entry.bind("<Return>", send_messages)

    send_button = tk.Button(root, text="Send message", command=send_message)
    send_button.pack(fill="x", padx=10, pady=10, side="bottom")  # Moved the send button to the bottom

    # Start the receive thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    root.mainloop()

except ConnectionRefusedError:
    print("Server is not running. Please start the server and try again.")

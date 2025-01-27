import socket as sock
import sys
import threading
from rich import print
from rich_utils import (
    print_welcome_message,
    print_exit_message,
    print_commands
)

HOST = '127.0.0.1'
PORT = 50000

sock_client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
sock_client.connect((HOST, PORT))

nickname = ""
while not nickname.strip():
    nickname = input("Please enter your name to join the Little Cat's Chat: ").strip()

sock_client.sendall(nickname.encode())

def listen_for_messages():
    while True:
        try:
            message = sock_client.recv(1024).decode()
            if message:
                print(f"{message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_message():
    while True:
        message = input(f"{nickname}: \n").strip()

        if message.lower() == "exit":
            print_exit_message()
            sock_client.sendall("exit".encode())
            sock_client.close()
            sys.exit()

        elif message.startswith("$"):
            parts = message.split(" ", 1)
            if len(parts) == 2:
                target_nickname = parts[0][1:]
                msg = parts[1]
                sock_client.sendall(f"${target_nickname} {msg}".encode())
            else:
                print("Invalid unicast format. Please use: $<nickname> <message>")
        else:
            sock_client.sendall(message.encode())

listener_thread = threading.Thread(target=listen_for_messages, daemon=True)
listener_thread.start()

print_welcome_message()
print_commands()

send_message()

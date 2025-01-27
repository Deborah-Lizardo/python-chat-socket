import socket as sock
import threading
from rich import print
from rich_utils import (
    print_exit_message,
    print_connection_established,
    print_no_clients_connected,
    print_client_list,
    print_message,
    print_socket_error,
    print_unexpected_error,
    print_closing_connection,
    print_server_started,
    print_welcome_message
)

HOST = '127.0.0.1'
PORT = 50000

clients = []  # List to store connected clients
chat_history = []  # List to store message history


# Function to send welcome message to the new client
def send_welcome(sock_conn, nickname):
    print_welcome_message()
    sock_conn.sendall(f"Welcome, {nickname} cat, to the Little Cats Gossip Chat!".encode())


# Function to handle client's nickname
def handle_nick(sock_conn, ender):
    while True:
        nickname = sock_conn.recv(1024).decode()
        if not nickname:
            sock_conn.sendall("Cat's name cannot be empty. Please try again.".encode())
            continue
        elif " " in nickname:
            sock_conn.sendall("Cat's name cannot contain spaces. Please try again.".encode())
            continue
        return nickname


# Function to handle messages
def handle_message(sock_conn, message, nickname, clients):
    message = message.strip()

    if message.lower() == "exit":
        sock_conn.sendall("You have left the Little Cats Gossip Chat.".encode())
        print_exit_message()
        return False

    elif message.lower() == "list":
        list_clients(sock_conn, clients)

    elif message.lower() == "see gossip":
        # Send message history when the client requests it
        send_chat_history(sock_conn)

    elif "$" in message:
        # Unicast logic (private message)
        recipient_nickname, msg = message.split("$", 1)
        recipient_nickname = recipient_nickname.strip()
        if recipient_nickname and msg.strip():
            send_private_message(recipient_nickname, msg.strip(), nickname, clients, sock_conn)
        else:
            sock_conn.sendall("Invalid private message format. Use: recipient_name $ message.".encode())

    else:
        # If the message is unknown or malformed
        if not message:
            sock_conn.sendall("Message cannot be empty. Please try again.".encode())
        else:
            # Broadcast: send the message to all other connected clients
            for client in clients:
                if client['connection'] != sock_conn:
                    try:
                        client['connection'].sendall(f"{nickname}: {message}".encode())
                        print_message(nickname, message)
                    except Exception as e:
                        print_socket_error(client['nickname'], e)

            # Add the message to the history
            chat_history.append(f"{nickname}: {message}")

    return True


# Function to send private message (unicast)
def send_private_message(recipient_nickname, message, sender_nickname, clients, sender_conn):
    recipient_conn = None
    for client in clients:
        if client['nickname'] == recipient_nickname:
            recipient_conn = client['connection']
            break
    if recipient_conn:
        try:
            recipient_conn.sendall(f"Private message from {sender_nickname}: {message}\n".encode())
            sender_conn.sendall(f"Private message sent to {recipient_nickname}: {message}\n".encode())
            print(f"Private message from {sender_nickname} to {recipient_nickname}: {message}")
        except Exception as e:
            print(f"Error sending private message: {e}")
    else:
        sender_conn.sendall(f"Cat '{recipient_nickname}' not found.\n".encode())


# Function to list connected clients
def list_clients(sock_conn, clients):
    if not clients:
        print_no_clients_connected()
        sock_conn.sendall("No cats connected.".encode())
        return
    client_list = "\n".join(client['nickname'] for client in clients)
    sock_conn.sendall(f"Connected clients:\n{client_list}".encode())
    print_client_list(clients)


# Function to remove a client from the list of connected clients
def remove_client(sock_conn, clients, nickname):
    for client in clients:
        if client['connection'] == sock_conn:
            print(f"[bold magenta]{nickname} cat has left the Little Cats chat![/bold magenta]")
            clients.remove(client)
            break


# Function to broadcast a message to all connected clients
def broadcast_message(message, clients):
    for client in clients:
        try:
            client['connection'].sendall(message.encode())
        except sock.error as e:
            print_socket_error(client['nickname'], e)


# Function to send chat history to the client who requests it
def send_chat_history(sock_conn):
    if not chat_history:
        sock_conn.sendall("No messages in the gossip yet.".encode())
        return

    # Send the message history to the client
    sock_conn.sendall("Chat history:\n".encode())
    for message in chat_history:
        sock_conn.sendall(message.encode())


# Function that manages communication with the client
def handle_client(sock_conn, ender, clients):
    nickname = handle_nick(sock_conn, ender)
    print(f"Connection established with {nickname} {ender}")
    print_connection_established(ender)

    try:
        send_welcome(sock_conn, nickname)

        broadcast_message(f"{nickname} cat has entered the Little Cats Chat!", clients)

        clients.append({"nickname": nickname, "connection": sock_conn, "address": ender})

        while True:
            message = sock_conn.recv(1024).decode()  # Receive the message from the client
            if not message:  # If there's no message or the connection is closed
                break
            should_continue = handle_message(sock_conn, message, nickname, clients)
            if not should_continue:  # If the client leaves
                break

    except sock.error as e:
        print_socket_error(ender, e)
    except Exception as e:
        print_unexpected_error(str(e))
    finally:
        print_closing_connection(ender)
        remove_client(sock_conn, clients, nickname)
        sock_conn.close()


# Function to start the server
def start_server():
    sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    sock_server.bind((HOST, PORT))
    sock_server.listen(5)
    print_server_started()  # Start server listening

    while True:
        try:
            sock_conn, ender = sock_server.accept()  # Accept a new client connection
            client_thread = threading.Thread(target=handle_client, args=(sock_conn, ender, clients))
            client_thread.start()  # Create a new thread to handle the client
        except sock.error as e:
            print(f"Error accepting connection: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    start_server()

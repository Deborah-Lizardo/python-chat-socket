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

clients = []  # Lista para armazenar clientes conectados
chat_history = []  # Lista para armazenar o histórico de mensagens


# Função para enviar boas-vindas ao novo cliente
def send_welcome(sock_conn, nickname):
    print_welcome_message()
    sock_conn.sendall(f"Welcome, {nickname} cat, to the Little Cats Gossip Chat!".encode())


# Função que recebe o apelido do cliente
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


# Função que lida com as mensagens
def handle_message(sock_conn, message, nickname, clients):
    message = message.strip()

    if message.lower() == "exit":
        sock_conn.sendall("You have left the Little Cats Gossip Chat.".encode())
        print_exit_message()
        return False

    elif message.lower() == "list":
        list_clients(sock_conn, clients)

    elif message.lower() == "see gossip":
        # Envia o histórico de mensagens quando o cliente pedir
        send_chat_history(sock_conn)

    elif "$" in message:
        # Lógica de unicast (mensagem privada)
        recipient_nickname, msg = message.split("$", 1)
        recipient_nickname = recipient_nickname.strip()
        if recipient_nickname and msg.strip():
            send_private_message(recipient_nickname, msg.strip(), nickname, clients, sock_conn)
        else:
            sock_conn.sendall("Invalid private message format. Use: recipient_name $ message.".encode())

    else:
        # Caso a mensagem seja algo desconhecido ou malformado
        if not message:
            sock_conn.sendall("Message cannot be empty. Please try again.".encode())
        else:
            # Broadcast: envia a mensagem para todos os outros clientes conectados
            for client in clients:
                if client['connection'] != sock_conn:
                    try:
                        client['connection'].sendall(f"{nickname}: {message}".encode())
                        print_message(nickname, message)
                    except Exception as e:
                        print_socket_error(client['nickname'], e)

            # Adiciona a mensagem no histórico
            chat_history.append(f"{nickname}: {message}")

    return True


# Função para enviar mensagem privada (unicast)
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


# Função para listar os clientes conectados
def list_clients(sock_conn, clients):
    if not clients:
        print_no_clients_connected()
        sock_conn.sendall("No cats connected.".encode())
        return
    client_list = "\n".join(client['nickname'] for client in clients)
    sock_conn.sendall(f"Connected clients:\n{client_list}".encode())
    print_client_list(clients)


# Função para remover o cliente da lista de clientes conectados
def remove_client(sock_conn, clients, nickname):
    for client in clients:
        if client['connection'] == sock_conn:
            print(f"[bold magenta]{nickname} cat has left the Little Cats chat![/bold magenta]")
            clients.remove(client)
            break


# Função para enviar uma mensagem para todos os clientes conectados
def broadcast_message(message, clients):
    for client in clients:
        try:
            client['connection'].sendall(message.encode())
        except sock.error as e:
            print_socket_error(client['nickname'], e)


# Função para enviar o histórico de mensagens para o cliente que pedir
def send_chat_history(sock_conn):
    if not chat_history:
        sock_conn.sendall("No messages in the gossip yet.".encode())
        return

    # Envia o histórico de mensagens para o cliente
    sock_conn.sendall("Chat history:\n".encode())
    for message in chat_history:
        sock_conn.sendall(message.encode())


# Função que gerencia a comunicação com o cliente
def handle_client(sock_conn, ender, clients):
    nickname = handle_nick(sock_conn, ender)
    print(f"Connection established with {nickname} {ender}")
    print_connection_established(ender)

    try:
        send_welcome(sock_conn, nickname)

        broadcast_message(f"{nickname} cat has entered the Little Cats Chat!", clients)

        clients.append({"nickname": nickname, "connection": sock_conn, "address": ender})

        while True:
            message = sock_conn.recv(1024).decode()  # Recebe a mensagem do cliente
            if not message:  # Se não houver mensagem ou a conexão for fechada
                break
            should_continue = handle_message(sock_conn, message, nickname, clients)
            if not should_continue:  # Se o cliente sair
                break

    except sock.error as e:
        print_socket_error(ender, e)
    except Exception as e:
        print_unexpected_error(str(e))
    finally:
        print_closing_connection(ender)
        remove_client(sock_conn, clients, nickname)
        sock_conn.close()


# Função que inicia o servidor
def start_server():
    sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    sock_server.bind((HOST, PORT))
    sock_server.listen(5)
    print_server_started()  # Inicia a escuta do servidor

    while True:
        try:
            sock_conn, ender = sock_server.accept()  # Aceita uma nova conexão de cliente
            client_thread = threading.Thread(target=handle_client, args=(sock_conn, ender, clients))
            client_thread.start()  # Cria uma nova thread para atender o cliente
        except sock.error as e:
            print(f"Error accepting connection: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    start_server()

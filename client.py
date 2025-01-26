import socket as sock
import sys
import threading
from rich import print
from rich_utils import (
    print_welcome_message,
    print_exit_message,
    print_comands
)

HOST = '127.0.0.1'
PORT = 50000

sock_client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
sock_client.connect((HOST, PORT))

nickname = ""
# Solicitar o nome do usuário até que ele forneça um nome válido
while not nickname.strip():  # Enquanto o nickname for vazio ou só espaços
    nickname = input("Please enter your name to join the Little Cat's Chat: ").strip()

sock_client.sendall(nickname.encode())  # Envia o nickname para o servidor


# Função para receber e exibir as mensagens do servidor
def listen_for_messages():
    while True:
        try:
            message = sock_client.recv(1024).decode()  # Recebe a mensagem do servidor
            if message:
                print(f"{message}")  # Exibe a mensagem recebida
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


# Função para enviar mensagens para o servidor (broadcast ou unicast)
def send_message():
    while True:
        message = input(f"{nickname}: \n").strip()

        if message.lower() == "exit":
            print_exit_message()
            sock_client.sendall("exit".encode())  # Envia comando de saída para o servidor
            sock_client.close()
            sys.exit()  # Encerra o cliente

        elif message.startswith("$"):
            # Lógica de unicast: verifica se a mensagem começa com "$"
            # O formato esperado é "$<nickname> <mensagem>"
            parts = message.split(" ", 1)
            if len(parts) == 2:
                target_nickname = parts[0][1:]  # Remove o "$" do início
                msg = parts[1]
                # Envia a mensagem privada (unicast) para o servidor
                sock_client.sendall(f"${target_nickname} {msg}".encode())
            else:
                print("Invalid unicast format. Please use: $<nickname> <message>")
        else:
            # Caso não seja unicast, é broadcast (enviado para todos)
            sock_client.sendall(message.encode())


# Cria uma thread para escutar mensagens do servidor (recebendo e mostrando no terminal)
listener_thread = threading.Thread(target=listen_for_messages, daemon=True)
listener_thread.start()

# Envia a primeira mensagem para iniciar o chat
print_welcome_message()
print_comands()

# Entra no loop principal de envio de mensagens
send_message()

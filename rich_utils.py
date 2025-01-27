from rich import print

def print_server_started():
    print("[bold magenta]Server started successfully! Listening for cats connections...[/bold magenta]")

def print_welcome_message():
    print(
        "[bold magenta]Welcome to the Little Cat's Chat! 🐾[/ bold magenta]")

def print_commands():
    print("[bold magenta]Here are the available commands:[/bold magenta]")
    print("[bold magenta]1. 'exit' - Leave the chat.[/bold magenta]")
    print("[bold magenta]2. 'list' - Show the list of currently connected clients.[/bold magenta]")
    print("[bold magenta]3. '<nickname> $ <message>' - Send a private message to a specific user (unicast) Format: $nickname message![/bold magenta]")
    print("[bold magenta]4. Any other message will be broadcasted to all users in the chat.[/bold magenta]")
    print("[bold magenta]Please note, we do not tolerate offensive language in our chat. We are all beautiful cats here, so be respectful! 😸[/bold magenta]")
    print("[bold magenta]Please note that all messages will be stored to verify compliance with our chat guidelines.[/bold magenta]")
    print("[bold magenta]Enjoy chatting with us![/bold magenta]")


def print_exit_message():
    print("[bold magenta]WAIT! THEY DON'T LOVE YOU LIKE I LOVE YOU! :( exiting the chat...[/bold magenta]")

def print_connection_established(ender):
    print(f"[bold magenta]Connection established with {ender}[/bold magenta]")

def print_no_clients_connected():
    print("[bold magenta]No clients connected.[/bold magenta]")

def print_client_list(clients):
    client_list = "\n".join(client['nickname'] for client in clients)
    print(f"[bold magenta]Connected clients:\n{client_list}[/bold magenta]")

def print_message(nickname, message):
    print(f"[bold magenta]{nickname}: {message}[/bold magenta]")

def print_socket_error(ender, error):
    print(f"[bold magenta]Socket error with client {ender}:{error}[/bold magenta]")

def print_unexpected_error(error_message):
    print(f"[bold magenta]Unexpected error occurred: {error_message}[/bold magenta]")

def print_socket_error(ender, error):
    print(f"[bold magenta]Socket error with client {ender}: {error}[/bold magenta]")

def print_closing_connection(ender):
    print(f"[bold magenta]Closing connection with {ender}[/bold magenta]")

def print_invalid_command():
    print("[bold magenta]Invalid command. Please try again.[/bold magenta]")


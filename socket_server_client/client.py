import socket
import datetime

from __config__ import *


def run_client() -> None:
    host_name = socket.gethostname()
    host_adress = socket.gethostbyname(host_name)

    client_socket = socket.socket()
    client_socket.connect((host_adress, PORT))

    # take inputted message
    message = input(" -> ")

    while message.lower().strip() != "--disconnect":
        client_socket.send(message.encode())

        server_response = client_socket.recv(KB_SIZE).decode()
        print(f"Server message: {str(server_response)}")

        message = input(" -> ")

    client_socket.close()


if __name__ == '__main__':
    run_client()

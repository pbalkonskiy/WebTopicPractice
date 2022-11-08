import socket

from config import *


def run_server():
    server_config = (LOCAL_ADRESS, PORT)

    print("Running server...\n")

    socket_obj = socket.socket()
    socket_obj.bind(server_config)
    print(f"Port {PORT} has been bind.")

    socket_obj.listen()
    print(f"Started listening port {PORT}.")

    conn, addr = socket_obj.accept()  # waiting for connection.
    local_addr, local_port = addr
    print(f"Successfully connected to {local_addr}:{local_port}.")

    while True:
        encoded_data = conn.recv(KB_SIZE)  # 1Kb of data awaited.
        conn.send(hash(encoded_data))
        data = encoded_data.decode("utf-8")
        if data[:4] == "exit()":
            break
        print(data, end="")

    conn.close()

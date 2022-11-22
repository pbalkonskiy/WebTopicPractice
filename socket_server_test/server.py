import socket
import json

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
        conn.send(encoded_data)
        data = encoded_data.decode("utf-8")

        if data[:4] == "exit":
            break

        elif data[:3] == "api":
            jdata = {
                "name": "server",
                "message": "200",
            }
            response = json.dumps(jdata).encode("utf-8")
            conn.send(response)

        elif data[:4] == "site":
            conn.send("""
            <h1>Server says: 200</h1>
            """.encode("utf-8"))

        print(data, end="")

    conn.close()

import socket
import datetime

from __config__ import *


def run_server() -> None:
    host_name = socket.gethostname()
    host_adress = socket.gethostbyname(host_name)

    server_socket = socket.socket()
    server_socket.bind((host_adress, PORT))

    # configure how many clients the server can listen simultaneously (here 2)
    server_socket.listen(2)
    conn, addr = server_socket.accept()
    client_addr, client_port = addr
    connection_time = datetime.datetime.now()

    print("Connection successful")
    print(f"Connection set at {connection_time}")
    print(f"From client: {client_addr}:{client_port}\n\n")

    while True:
        # receive data stream & send response to the client
        data_received = conn.recv(KB_SIZE).decode()
        if not data_received:
            break
        print(f"Client message: {str(data_received)}  --  at {datetime.datetime.now()}")
        data_respond = input(" -> ")
        conn.send(data_respond.encode())

    disconnection_time = datetime.datetime.now()
    print(f"Disconnected at {disconnection_time}")
    print(f"Session time: {disconnection_time - connection_time}")
    conn.close()


if __name__ == "__main__":
    run_server()

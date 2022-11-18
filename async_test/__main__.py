import socket


def main() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    server_socket.bind(("localhost", 5000))
    server_socket.listen()

    while True:
        print("Before .accept()")
        client_conn, addr = server_socket.accept()
        print("Connection from", addr)

        while True:
            request = client_conn.recv(4096)

            if request:
                response = "Hello, client!\n".encode()
                client_conn.send(response)
            else:
                break

        print("Process terminated.")
        client_conn.close()


if __name__ == '__main__':
    main()

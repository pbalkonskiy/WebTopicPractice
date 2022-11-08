import socket

from config import *


def parse_request(request: str) -> tuple[str, str]:
    """
    Parses decoded user request block;
    gets tuple of HTTP-method & URL.
    :param request: str
    :return: method: str, url: str
    """

    parsed = request.split(" ")
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method: str, url: str) -> tuple[str, int]:
    """
    Contains required conditionals
    to check passed HTTP-method & URL.
    :param method: str
    :param url: str
    :return: headers: str, code: int
    """

    if not method == "GET":
        return "HTTP/1.1 405 Method not allowed.\n\n", 405
    if url not in URLS:
        return "HTTP/1.1 404 Not found\n\n", 404
    return "HTTP/1.1 200 OK\n\n", 200


def generate_content(code: int, url: str) -> str:
    """
    Contains required conditionals
    to check passed code values;
    generates HTML body if successful.
    :param code: int
    :param url: str
    :return: str
    """
    if code == 404:
        return "<h1>404</h1><p>Not found</p>"
    if code == 405:
        return "<h1>405</h1><p>Method not allowed</p>"
    return f"<h1>{URLS[url]}</h1>"


def generate_response(request: str) -> bytes:
    """
    Manages to parse a request with parse_request(),
    gets HTTP-method & URL, uses them to
    generate headers in generate_headers().
    :param request: str
    :return: headers: bytes
    """

    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)
    return (headers + body).encode()


def run_server() -> None:
    server_config = ("localhost", PORT)

    # socket.AF_INET - IPV4, socket.SOCK_STREAM - TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(server_config)
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(KB_SIZE)
        print(request.decode("utf-8"), "\n", addr)

        response = generate_response(request.decode("utf-8"))

        client_socket.sendall(response)
        client_socket.close()

import urllib.parse
import logging
import socket
import pathlib
import mimetypes

from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process


def send_data_to_socket(address, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as http_server:
        http_server.connect((address, port))
        logging.info("Sending to socket")
        http_server.sendall(data)
        logging.info("Receive answer")
        answer = http_server.recv(1024)
        logging.info(str(answer))
        http_server.close()


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        data = self.rfile.read(int(self.headers["Content-Length"]))

        socket_client = Process(
            target=send_data_to_socket, args=("localhost", 5000, data)
        )
        socket_client.start()
        logging.info("HTTP Server: socket client started")

        socket_client.join()
        logging.info("HTTP Server: socket client closed")

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("templates/index.html")
        elif pr_url.path == "/message":
            self.send_html_file("templates/message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("templates/error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def run_http_server(address, port, server_class=HTTPServer, handler_class=HttpHandler):
    http = server_class((address, port), handler_class)
    try:
        logging.info(f"HTTP server started on port {address}:{port}")
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

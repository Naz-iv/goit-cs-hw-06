from multiprocessing import Process
import logging
from http_server import run_http_server
from socket_server import run_socket_server


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    logging.info("Socket server starting...")
    socket_server = Process(target=run_socket_server, args=("0.0.0.0", 5000))
    socket_server.start()
    logging.info("HTTP server starting...")
    http_server = Process(target=run_http_server, args=("0.0.0.0", 3000))
    http_server.start()

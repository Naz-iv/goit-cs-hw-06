import logging
import socket
import urllib.parse

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from multiprocessing import Process


def save_data(data):
    client = MongoClient("mongodb://root:example@0.0.0.0:27017", server_api=ServerApi("1"))
    db = client.db
    logging.info("Saving message information to Mongo...")
    data_parse = urllib.parse.unquote_plus(data.decode())
    try:
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        data_dict["date"] = str(datetime.now())
        logging.info(data_dict)
        db.messages.insert_one(data_dict)
        logging.info("Message writen to database.")

    except Exception as e:
        logging.error(e)
    finally:
        client.close()


def run_socket_server(ip, port):
    addr = (ip, port)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(addr)
            server.listen()
            logging.info(f"Socket server started on {ip}:{port}")
            while True:
                server_connection = server.accept()
                data = server_connection[0].recv(1024)
                logging.debug(data)

                save_data_process = Process(
                    target=save_data, args=(data,)
                )
                save_data_process.start()

                server_connection[0].close()
    except Exception as e:
        logging.error(f"Error in socket server: {e}")
    finally:
        if server:
            server.close()
            logging.info("Socket server closed")

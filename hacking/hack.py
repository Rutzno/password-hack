import argparse
import itertools
import socket
import sys

"""
__author__ = "Mack_TB"
__since__ = "28/8/2021"
__version__ = "1.0.2"
"""


def get_arguments():
    parser = argparse.ArgumentParser(description="A script to guess password")
    parser.add_argument("hostname", type=str, help="IP address or domain name")
    parser.add_argument("port", type=int, help="Port number")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_arguments()

    with socket.socket() as client_socket:  # creating the socket with context manager
        hostname = args.hostname
        port = args.port
        address = (hostname, port)

        client_socket.connect(address)  # connecting to the server

        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        i = 1
        response = ""
        while response != "Connection success!":
            for tup in itertools.product(chars, repeat=i):
                password = "".join(tup)
                client_socket.send(password.encode())  # sending through socket

                response = client_socket.recv(1024)  # receiving the response
                response = response.decode()  # decoding from bytes to string
                if response == "Connection success!":
                    print(password)
                    break
            i += 1


import socket
import sys

"""
__author__ = "Mack_TB"
__since__ = "28/8/2021"
__version__ = "1.0.1"
"""

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 4:
        print("The script should be called with three arguments, the hostname, the port and the data to send")
    else:
        with socket.socket() as client_socket:  # creating the socket with context manager
            hostname = args[1]
            port = int(args[2])
            address = (hostname, port)

            client_socket.connect(address)  # connecting to the server

            data = args[3].encode()  # converting to bytes

            client_socket.send(data)  # sending through socket

            response = client_socket.recv(1024)  # receiving the response
            response = response.decode()  # decoding from bytes to string

            print(response)

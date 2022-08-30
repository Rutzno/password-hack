import socket
import sys

"""
__author__ = "Mack_TB"
__since__ = "28/8/2021"
__version__ = "1.0.2"
"""

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 3:
        print("The script should be called with two arguments, the hostname and the port to connect to the server")
    else:
        with socket.socket() as client_socket:  # creating the socket with context manager
            hostname = args[1]
            port = int(args[2])
            address = (hostname, port)

            client_socket.connect(address)  # connecting to the server

            chars = "abcdefghijklmnopqrstuvwxyz0123456789"

            i = 1
            while i <= 1000000:
                for s in itertools.product(chars, repeat=i):
                    password = "".join(s)
                    client_socket.send(password.encode())  # sending through socket

                    response = client_socket.recv(1024)  # receiving the response
                    response = response.decode()  # decoding from bytes to string
                    if response == "Connection success!":
                        print(password)
                        break
                i += 1

            # password = args[3].encode()  # converting to bytes
            #
            # client_socket.send(password)  # sending through socket
            #
            # response = client_socket.recv(1024)  # receiving the response
            # response = response.decode()  # decoding from bytes to string
            #
            # print(response)

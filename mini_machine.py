import sys
import os
import socket
import time
import socket


receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

send_sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM)]

if len(sys.argv) != 2:
    print("Usage: python machine.py machine_id")
    exit(0)

port = int(sys.argv[1])


def receive():
    receive_socket.bind(('localhost', 50050 + port))
    receive_socket.listen(2)
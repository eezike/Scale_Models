import sys
import os
import socket
from configuration import Configuration
import threading
import time
from  logical_clock import LogicalClock

class Machine:
    def __init__(self, machine_id) -> None:
        self.machine_id = machine_id
        self.config = Configuration(machine_id)

        self.queue = []
        self.stop_event = threading.Event()
        self.log_file = open(f"machine{machine_id}.log", "w")

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM)]

        # create threads for listening and sending messages
        self.receive_thread: threading.Thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.send_thread: threading.Thread = threading.Thread(target=self.send_loop, daemon=True)

    def connect(self):
        self.receive_socket.bind((self.config.HOST, self.config.port))
        self.receive_socket.listen(self.config.NUM_PROCESSES - 1)

        if len(self.send_sockets) != len(self.config.peer_ports):
            print("peer ports and send sockets do not match")
            os._exit(1)

        def connect_loop(port, sock_idx):
            while True:
                try:
                    self.send_sockets[sock_idx].bind((self.config.HOST, port))
                    self.receive_socket.listen(1)
                except socket.error as msg:
                    print("Socket binding error: " + str(msg) + "\n" + "Retrying in 15 secs...")
                    time.sleep(15)

        for i, peer_port in enumerate(self.config.peer_ports):
            threading.Thread(target = connect_loop, args=(peer_port, i)).start()

    def start(self):
        # start listening and sending threads
        self.receive_thread.start()
        self.send_thread.start()

    def stop(self):
        # set stop event to stop threads
        self.stop_event.set()

    def receive_loop(self):

        self.receive_socket.bind((self.HOST, self.PORT))
        self.receive_socket.listen(2)

        time.sleep(2)

        clientsockets = []
        
        while True:
            # accepts a client socket request
            clientsocket, addr = self.server.accept()
            print(f"{self.machine_id}: {addr[0]} has joined")
            clientsockets.append(clientsocket)

            threading.Thread(target = self.handle_client, args = (clientsocket, addr)).start()

    def handle_client(self, clientsocket: socket.socket):
        while not self.stop_event.is_set():
            # TODO: receive messages from network queue and update logical clock
            pass
    
    def send_loop(self):
        while not self.stop_event.is_set():
            # TODO: send messages to other machines with random probabilities
            pass    

    def log_event(self, event_type, timestamp):
        # TODO: log event to file with machine id, event type, timestamp, queue length, and logical clock value
        pass

def initMachine():
    if len(sys.argv) != 2:
        print("Usage: python machine.py machine_id")
        return

    machine_id = sys.argv[1]
    machine = Machine(machine_id)

if __name__ == '__main__':
    initMachine()
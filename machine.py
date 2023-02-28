import threading
import time
import random
import socket
from  logical_clock import LogicalClock

# define the number of machines in the system
NUM_MACHINES = 3

class Machine:
    def __init__(self, machine_id: int, clock_rate: int):
        self.machine_id = machine_id
        self.clock_rate = clock_rate
        self.clock = LogicalClock()
        self.queue = []
        self.log_file = open(f"machine{machine_id}.log", "w")
        self.stop_event = threading.Event()


        self.receive_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM)]
        
        # create threads for listening and sending messages
        self.receive_thread: threading.Thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.send_thread: threading.Thread = threading.Thread(target=self.send_loop, daemon=True)
        
        # connect to all other machines in the system
        self.connections = []
        for i in range(NUM_MACHINES):
            if i != self.machine_id:
                self.connections.append(i) # connect to machine i
    
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


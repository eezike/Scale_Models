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
        self.clock = LogicalClock()
        self.queue = []
        self.log_file = open(f"machine{machine_id}.log", "w")
        self.stop_event = threading.Event()

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM)]

        self.receive_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.lock = threading.Lock()

        self.start()

    def start(self):
        self.receive_thread.start()
        self.connect()

    def stop(self):
        self.stop_event.set()

    def connect(self):
        if len(self.send_sockets) != len(self.config.peer_ports):
            print("Peer ports and send sockets do not match")
            os._exit(1)

        def connect_loop(port, sock_idx):
            # Try connecting every 15 seconds
            while True:
                try:
                    self.send_sockets[sock_idx].connect((self.config.HOST, port))
                    break
                except socket.error as msg:
                    print(f"Socket binding error: " + str(msg) + "\n" + "Retrying in 15 secs...")
                    time.sleep(15)
            
            # Once connected, switch to sending messages
            print("Connected to machine at: " + str(port))
            self.send_loop(self.send_sockets[sock_idx])

        # Connect to each machine in a separate thread
        for i, peer_port in enumerate(self.config.peer_ports):
            threading.Thread(target = connect_loop, args=(peer_port, i)).start()

    def receive_loop(self):

        self.receive_socket.bind((self.config.HOST, self.config.port))
        self.receive_socket.listen(self.config.NUM_PROCESSES - 1)

        clientsockets = []
        
        while True:
            # accepts a client socket request
            clientsocket, addr = self.receive_socket.accept()
            print(f"{self.machine_id}: {addr[0]} has joined")
            clientsockets.append(clientsocket)
            threading.Thread(target = self.handle_client, args = (clientsocket, addr)).start()

    def handle_client(self, clientsocket: socket.socket):
        while not self.stop_event.is_set():
            # TODO: receive messages from network queue and update logical clock
            pass
    
    def send_loop(self, ):
        while not self.stop_event.is_set():
            # TODO: send messages to other machines with random probabilities
            pass    

    def log_event(self, event_type, timestamp):
        # TODO: log event to file with machine id, event type, timestamp, queue length, and logical clock value
        queue_length = len(self.queue)
        system_time = time.time()
        log_entry = f"[{system_time}] Machine {self.machine_id} received an {event_type} message, queue length: {queue_length}, logical clock time: {self.clock.time}\n"

        # write the log entry to the log file
        self.log_file.write(log_entry)
        self.log_file.flush()

def initMachine():
    if len(sys.argv) != 2:
        print("Usage: python machine.py machine_id")
        return

    machine_id = sys.argv[1]
    machine = Machine(machine_id)

if __name__ == '__main__':
    initMachine()
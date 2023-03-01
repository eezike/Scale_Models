import sys
import os
import socket
from configuration import Configuration
import threading
import time
import random
from  logical_clock import LogicalClock

class Machine:
    def __init__(self, machine_id) -> None:
        self.machine_id = machine_id
        self.config = Configuration(machine_id)
        self.clock = LogicalClock()
        self.queue = []

        log_dir = "/logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_file = open(f"{log_dir}/machine{machine_id}.log", "a+")

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM)]

        self.receive_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.send_thread = threading.Thread(target=self.send_loop, daemon=True)
        self.stop_event = threading.Event()
        self.lock = threading.Lock()

        self.start()

    # Start machine
    def start(self):
        self.receive_thread.start()
        self.connect()
        self.send_thread.start()

    # Stop machine
    def stop(self):
        self.stop_event.set()

    # Connect to all other machines
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

        for i, peer_port in enumerate(self.config.peer_ports):
            # Connect to each machine in a separate thread
            threading.Thread(target = connect_loop, args=(peer_port, i)).start()

    # Start receiving and handling clients
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
            # Receive messages and put them into the queue
            try:
                # Receive the message from the client
                message = clientsocket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                # Add the message to the queue
                self.queue.append(message)
            
            except socket.error as msg:
                # Handle case when the client abruptly terminates the connection
                print(msg)
    
        # Clean up the client socket
        clientsocket.close()
    
    def send_loop(self):
        # Send messages to other machines with random probabilities
        while not self.stop_event.is_set():

            # Choose a message event between 1-10
            event = random.randint(1, 11)
            message = self.clock.time # TODO: we probably want to send the machine ID here too

            """
            Event 1: Send the message to a machine
            Event 2: Send the message to the other machine (not from event 1)
            Event 3: Send the message to both of the other machines
            Events 4-10: Internal clock updates
            """
            if event == 1:
                self.send_sockets[0].sendall(message.encode())
            elif event == 2:
                self.send_sockets[1].sendall(message.encode())
            elif event == 3:
                for sock in self.send_sockets:
                    sock.sendall.sendall(message.encode())
            else:
                pass

            self.log_event(event)

    def log_event(self, event_type):
        # Log event to file with machine id, event type, timestamp, queue length, and logical clock value
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
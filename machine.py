import sys
import os
import socket
from configuration import Configuration
import threading
import time
import random
from  logical_clock import LogicalClock
        
class Machine:
    HOST = "localhost"
    NUM_PROCESSES = 2

    def __init__(self, machine_id) -> None:
        self.machine_id = int(machine_id)
        
        # Initialize the machine's clock
        self.clock = LogicalClock()

        self.queue = []

        # Create the log file
        log_dir = "/logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_file = open(f"{log_dir}/machine{machine_id}.log", "a+")

        # Define the machine's port and the port of other processes
        self.peer_ports = [50050, 50051, 50052]
        self.port = 50049 + self.machine_id
        self.peer_ports.remove(self.port)
        

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.send_sockets = {}

        for port in self.peer_ports:
            self.send_sockets[port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Keep track of connected sockets 
        self.connected = 0

        # Define the threads for receiving and sending messages
        self.receive_thread = threading.Thread(target=self.receive_loop)
        self.send_thread = threading.Thread(target=self.send_loop)
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.start()

    # Start machine
    def start(self):
        self.receive_thread.start()
        print("Connecting in 10 seconds...")
        time.sleep(10)
        self.connect()
        print("All connected, starting to send...")
        self.send_thread.start()

    # Stop machine
    def stop(self):
        self.stop_event.set()

    # Connect to all other machines
    def connect(self):
        print("Connecting now...")
        if len(self.send_sockets) != len(self.peer_ports):
            print("Peer ports and send sockets do not match")
            os._exit(1)
        
        for port in self.peer_ports:
            while True:
                try:
                    self.send_sockets[port].connect((self.HOST, port))
                    break
                except socket.error as msg:
                    print(f"Socket binding error: " + str(msg) + "\n" + "Retrying in 30 secs...")
                    time.sleep(10)

    # Start receiving and handling clients
    def receive_loop(self):

        self.receive_socket.bind((self.HOST, self.port))
        self.receive_socket.listen(self.NUM_PROCESSES - 1)

        clientsockets = []
        
        while True:
            # accepts a client socket request
            clientsocket, addr = self.receive_socket.accept()
            print(f"{self.machine_id}: {addr[0]} has joined")
            clientsockets.append(clientsocket)
            threading.Thread(target = self.handle_client, args = (clientsocket,), daemon = True).start()

    def handle_client(self, clientsocket):
        try:
            while not self.stop_event.is_set():
                try:
                    # Receive the message from the client
                    message = clientsocket.recv(4)
                    message = int.from_bytes(message, 'big')
                    print(message)
                    if not message:
                        break
                    
                    # Add the message to the queue
                    self.queue.append(message)
            
                except socket.error as msg:
                    # Handle case when the client abruptly terminates the connection
                    print(msg)

        except KeyboardInterrupt:
            print("Exiting..")

    def send_loop(self):
        # Send messages to other machines with random probabilities
        while not self.stop_event.is_set():

            # Choose a message event between 1-10
            event = random.randint(1, 3)
            message = self.clock.get_time() + self.machine_id * 1000 # TODO: we probably want to send the machine ID here too
            message =  message.to_bytes(2, 'big')

            """
            Event 1: Send the message to a machine
            Event 2: Send the message to the other machine (not from event 1)
            Event 3: Send the message to both of the other machines
            Events 4-10: Internal clock updates
            """
            if event == 1:
                self.send_sockets[self.peer_ports[0]].sendall(message)
            elif event == 2:
                self.send_sockets[self.peer_ports[1]].sendall(message)
            elif event == 3:
                for sock in self.send_sockets.values():
                    sock.sendall(message)
            else:
                pass

            # self.log_event(event)

    def log_event(self, event_type):
        # Log event to file with machine id, event type, timestamp, queue length, and logical clock value
        queue_length = len(self.queue)
        system_time = time.time()
        log_entry = f"[{system_time}] Machine {self.machine_id} received an {event_type} message, queue length: {queue_length}, logical clock time: {self.clock.get_time()}\n"

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
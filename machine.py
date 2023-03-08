import sys
import os
import socket
import threading
import time
from datetime import datetime
import random
from  logical_clock import LogicalClock
import struct
import queue
        
class Machine:
    HOST = "localhost"
    NUM_PROCESSES = 3
    CONNECTION_WAIT = 10

    def __init__(self, machine_id: int, silent: bool = False, clock_rate: int = None, log_dir: str = "logs", ) -> None:

        self.SILENT = silent

        self.MACHINE_ID = machine_id

        # Only allow for machine_ids between 1 and 3 inclusive
        if machine_id < 1 or machine_id > 3:
            self.pprint("Only create machines with ids between 1 and 3 inclusive")
            exit(1)
        
        # Initialize the machine's clock
        self.clock = LogicalClock(clock_rate)
        self.pprint(f"Clock rate: {self.clock.clock_rate}")

        # Create the message queue
        self.message_queue = queue.Queue()

        # Create the log file
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_file = open(f"{log_dir}/machine{self.MACHINE_ID}.log", "w")

        # Define the machine's port and the port of other processes
        self.PEER_PORTS = [50050, 50051, 50052]
        self.PORT = 50049 + self.MACHINE_ID
        self.PEER_PORTS.remove(self.PORT)
        
        # Initialize the socket for receiving messages
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Initialize a dict where sockets for sending messagese are values, and the key's are the recipients' ports
        self.send_sockets: dict[int, socket.socket] = {}
        for port in self.PEER_PORTS:
            self.send_sockets[port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Mark if socket is fully connected
        self.connected = False

        # Define the threads for receiving and sending messages
        self.receive_thread = threading.Thread(target=self.receive_loop)
        self.send_thread = threading.Thread(target=self.send_loop)
        self.stop_event = threading.Event()
        
        # Log the machine's initial clock rate
        self.log_event("initial")
    
    def pprint(self, content, end = "\n"):
        if not self.SILENT:
            print(f"Machine {self.MACHINE_ID}: {content}", end= end)
    
    # Initialize connections and start sending process
    def run(self):
        self.pprint(f"Connecting in {self.CONNECTION_WAIT} seconds...")
        time.sleep(self.CONNECTION_WAIT)
        self.connect()
        
        while self.connected == False:
           time.sleep(0.001)

        self.pprint("All connected; starting now")
        self.send_thread.start()
        for i in range(60, -1, -1):
            if i % 3 == (self.MACHINE_ID - 1):
                self.pprint(i)
            time.sleep(1)
        self.stop()


    # Stop machine
    def stop(self):
        self.connected = True
        self.close()
        self.stop_event.set()

    # Close all sockets and log files in machine
    def close(self):
        self.receive_socket.close()
        for sock in self.send_sockets.values():
            sock.close()

        self.log_file.close()

    # Connect to all other machines
    def connect(self):
        self.pprint("Connecting now...")
        self.receive_thread.start()
        
        for port in self.PEER_PORTS:
            while True:
                try:
                    self.send_sockets[port].connect((self.HOST, port))
                    break
                except socket.error as msg:
                    self.pprint(f"Socket binding error: " + str(msg) + "\n" + "Retrying in 5 secs...")
                    time.sleep(5)

    # Start receiving and handling clients
    def receive_loop(self):

        self.receive_socket.bind((self.HOST, self.PORT))
        self.receive_socket.listen(self.NUM_PROCESSES - 1)
        
        for _ in range(self.NUM_PROCESSES - 1):
            # accepts a client socket request
            clientsocket, addr = self.receive_socket.accept()
            self.pprint(f"{addr[0]} has joined")
            threading.Thread(target = self.handle_client, args = (clientsocket, addr)).start()

        self.connected = True

    def handle_client(self, clientsocket: socket.socket, addr) -> None:
        try:
            while not self.stop_event.is_set():

                # Receive the message from the client
                data = clientsocket.recv(4)
                if not data:
                    raise BrokenPipeError
                
                message: int = struct.unpack("i", data)[0]

                # Add the message to the queue
                self.message_queue.put(message)
        except (KeyboardInterrupt, BrokenPipeError, BrokenPipeError):
            self.pprint(addr[0] + ' disconnected unexpectedly')
        finally:
            # Close the client socket
            clientsocket.close()
            self.stop()

    def send_loop(self, force_event = None):
        # Send messages to other machines with random probabilities
        try:
            while not self.stop_event.is_set():

                self.clock.tick()

                if not self.message_queue.empty():
                    new_time = self.message_queue.get()
                    self.clock.update(new_time)
                    self.log_event("receive")
                    continue

                # Choose a message event between 1-10 (force event for testing purposes)
                event = force_event if force_event != None else random.randint(1, 10)

                # Pack the message as an integer (as we only send the clock time)
                message =  struct.pack("i", self.clock.get_time())

                """
                Event 1: Send the message to a machine
                Event 2: Send the message to the other machine (not from event 1)
                Event 3: Send the message to both of the other machines
                Events 4-10: Internal clock updates
                """
                if event == 1:
                    self.send_sockets[self.PEER_PORTS[0]].sendall(message)
                    event = "send"
                elif event == 2:
                    self.send_sockets[self.PEER_PORTS[1]].sendall(message)
                    event = "send"
                elif event == 3:
                    for sock in self.send_sockets.values():
                        sock.sendall(message)
                    event = "send"
                else:
                    event = "internal"
                
                self.log_event(event)
        except (KeyboardInterrupt, BrokenPipeError, OSError):
            self.pprint("Broken pipe")
        finally:
            self.stop()

    def log_event(self, event_type = "internal"):
        # Log event to file with machine id, event type, timestamp, queue length, and logical clock value
        queue_length = self.message_queue.qsize()

        # Get the system's time in H:M:S format
        system_time = datetime.now()
        system_time = system_time.strftime("%H:%M:%S")

        if event_type == "initial":
            log_entry = f"[Machine initialized with clock_rate: {self.clock.clock_rate}]\n"
        elif event_type == "receive":
            log_entry = f"[{event_type}_event, {system_time}, {queue_length}, {self.clock.get_time()}]\n"
        elif event_type == "send":
            log_entry = f"[{event_type}_event, {system_time}, {self.clock.get_time()}]\n"
        else:
            log_entry = f"[internal_event, {system_time}, {self.clock.get_time()}]\n"

        # write the log entry to the log file
        try:
            self.log_file.write(log_entry)
            self.log_file.flush()
        except:
            pass

# Creates machine with specified id via command terminal args
def create_machine(machine_id = None, silent = False) -> Machine:
    if machine_id == None:
        if len(sys.argv) != 2:
            print("Usage: python machine.py machine_id")
            exit(1)

        try:
            machine_id = int(sys.argv[1])
        except:
            print("Usage: python machine.py machine_id:int")
            exit(1)
    
    return Machine(machine_id, silent=silent)

def main(id=None):
    machine = create_machine(id)
    machine.run()

if __name__ == '__main__':
    main()
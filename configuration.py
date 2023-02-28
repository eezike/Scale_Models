import random

class Configuration:

    def __init__(self, process_id):
        self.process_id = process_id
        
        # Define the ports for each process
        if self.process_id == 1:
            self.port = 8000
            self.peer_ports = [8001, 8002]
        elif self.process_id == 2:
            self.port = 8001
            self.peer_ports = [8000, 8002]
        elif self.process_id == 3:
            self.port = 8002
            self.peer_ports = [8000, 8001]
        else:
            raise ValueError("Invalid process ID")
            
        # Define other configuration variables
        self.host = "localhost"
        self.clock_rate = random.randint(1, 6)
        self.log_file = f"process_{self.process_id}.log"
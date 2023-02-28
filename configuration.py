import random

class Configuration:

    HOST = "localhost"
    NUM_PROCESSES = 3

    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.clock_rate = random.randint(1, 6)
        print(f"{self.machine_id}'s clock rate: {self.clock_rate}")
        
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
            
        self.clock_rate = random.randint(1, 6)
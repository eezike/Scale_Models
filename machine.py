import sys
import socket
from configuration import Configuration

class Machine:
    def __init__(self, process_id) -> None:
        self.process_id = process_id
        self.configs = Configuration(process_id)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Yes/No printing
		self.SILENT = silent 

		# retreives hostname on host computer
		self.HOST = socket.gethostname()

		# retreives IP on host computer
		self.IP = socket.gethostbyname(self.HOST)




def initMachine():
    if len(sys.argv) != 2:
        print("Usage: python machine.py process_id")
        return

    process_id = sys.argv[1]
    machine = Machine(process_id)

if __name__ == '__main__':
    initMachine()

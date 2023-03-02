from machine import Machine
import threading

NUM_MACHINES = 3

machines = [Machine(i+1) for i in range(NUM_MACHINES)]

connect_threads = [threading.Thread(target = machines[i].init_connection) for i in range(NUM_MACHINES)]
for t in connect_threads:
    t.start()

for t in connect_threads:
    t.join()

print("Done")


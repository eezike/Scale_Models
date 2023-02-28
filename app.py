from machine import Machine
import random 
import time
from machine import NUM_MACHINES

# create machines with random clock rates
machines = []
for i in range(NUM_MACHINES):
    clock_rate = random.randint(1, 6)
    machine = Machine(i, clock_rate)
    machines.append(machine)

# start machines
for machine in machines:
    machine.start()

# run for a fixed duration
DURATION = 60 # seconds
start_time = time.monotonic()
while time.monotonic() - start_time < DURATION:
    time.sleep(1)

# stop machines and wait for threads to join
for machine in machines:
    machine.stop()
for machine in machines:
    machine.receive_thread.join()
    machine.send_thread.join()

from machine import Machine
import threading

NUM_MACHINES = 3

machines = [Machine(i+1) for i in range(NUM_MACHINES)]

connect_threads = [threading.Thread(target = machines[i].init_connection, daemon=True) for i in range(NUM_MACHINES)]
for t in connect_threads:
    t.start()

for t in connect_threads:
    t.join()

print("Done")

# Multiprocessing code does not work on Windows
# from machine import Machine
# import multiprocessing

# if __name__ == '__main__':
#     NUM_MACHINES = 3
#     processes = []
#     for i in range(NUM_MACHINES):
#         machine = Machine(i+1)
#         process = multiprocessing.Process(target=machine.init_connection)
#         processes.append(process)

#     for process in processes:
#         process.start()

#     for process in processes:
#         process.join()

#     print("Done")
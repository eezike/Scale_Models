from machine import Machine, main
import multiprocessing

if __name__ == '__main__':
    NUM_MACHINES = 3
    processes = []
    
    # Spawns a new process for each machine that we have to run 
    for i in range(NUM_MACHINES):
        process = multiprocessing.Process(target=main, args=(i+1,))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print("Done")
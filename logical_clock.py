import time
import random

class LogicalClock:
    def __init__(self, clock_rate = None):
        self._time: int = 0
        self.clock_rate = clock_rate if clock_rate != None else random.randint(1, 6)
    
    def tick(self):
        self._time += 1
        time.sleep(1 / self.clock_rate)

    def update(self, new_time: int):
        self._time = max(self._time, new_time) + 1

    def get_time(self):
        return self._time
        
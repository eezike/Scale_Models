import time
import random

class LogicalClock:
    def __init__(self):
        self._time: int = 0
        clock_rate = random.randint(1, 6)
        print(f"Clock rate: {clock_rate}")
        self.delayer = clock_rate
    
    def tick(self):
        # self._time += 1

        # if self._time % self.delayer == 0:
        #     time.sleep(1)
        pass
    
    def update(self, new_time: int):
        self._time = max(self.time, new_time) + 1

    def get_time(self):
        return self._time
        
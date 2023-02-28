
class LogicalClock:
    def __init__(self):
        self.time: int = 0
    
    def tick(self):
        self.time += 1
    
    def update(self, new_time: int):
        self.time = max(self.time, new_time) + 1
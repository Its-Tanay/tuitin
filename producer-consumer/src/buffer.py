import threading

class SharedBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.condition = threading.Condition()
        self.production_complete = False

    def put(self, item):
        with self.condition:
            while len(self.buffer) >= self.capacity:
                self.condition.wait()

            self.buffer.append(item)
            self.condition.notify()

    def get(self):
        with self.condition:
            while len(self.buffer) == 0 and not self.production_complete:
                self.condition.wait()

            if len(self.buffer) == 0:
                return None

            item = self.buffer.pop(0)
            self.condition.notify()
            return item

    def mark_complete(self):
        with self.condition:
            self.production_complete = True
            self.condition.notify()

    def size(self):
        return len(self.buffer)

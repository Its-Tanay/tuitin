import time

class Consumer:
    def __init__(self, shared_buffer, delay=0, on_consume=None):
        self.shared_buffer = shared_buffer
        self.delay = delay
        self.on_consume = on_consume
        self.consumed_items = []
        self.items_consumed = 0

    def run(self):
        while True:
            item = self.shared_buffer.get()
            if item is None:
                break

            self.consumed_items.append(item)
            self.items_consumed += 1

            if self.on_consume:
                self.on_consume(item, self.items_consumed, self.shared_buffer.size())

            if self.delay > 0:
                time.sleep(self.delay)

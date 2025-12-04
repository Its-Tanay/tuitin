import time

class Producer:
    def __init__(self, shared_buffer, source_data, delay=0, on_produce=None):
        self.shared_buffer = shared_buffer
        self.source_data = source_data
        self.delay = delay
        self.on_produce = on_produce
        self.items_produced = 0

    def run(self):
        for item in self.source_data:
            self.shared_buffer.put(item)
            self.items_produced += 1

            if self.on_produce:
                self.on_produce(item, self.items_produced, self.shared_buffer.size())

            if self.delay > 0:
                time.sleep(self.delay)

        self.shared_buffer.mark_complete()

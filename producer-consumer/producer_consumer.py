import threading
import time


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


class Producer:
    def __init__(self, shared_buffer, source_data):
        self.shared_buffer = shared_buffer
        self.source_data = source_data
        self.items_produced = 0

    def run(self):
        for item in self.source_data:
            self.shared_buffer.put(item)
            self.items_produced += 1
            print(f"[Producer] Produced message {item['id']} | Buffer: {self.shared_buffer.size()}/{self.shared_buffer.capacity}")
            time.sleep(0.1)

        self.shared_buffer.mark_complete()
        print(f"[Producer] Completed - {self.items_produced} items produced")


class Consumer:
    def __init__(self, shared_buffer):
        self.shared_buffer = shared_buffer
        self.consumed_items = []
        self.items_consumed = 0

    def run(self):
        while True:
            item = self.shared_buffer.get()
            if item is None:
                break

            self.consumed_items.append(item)
            self.items_consumed += 1
            print(f"[Consumer] Consumed message {item['id']} | Buffer: {self.shared_buffer.size()}/{self.shared_buffer.capacity}")
            time.sleep(0.15)

        print(f"[Consumer] Completed - {self.items_consumed} items consumed")


def create_messages(count):
    messages = []
    priorities = ['high', 'medium', 'low']

    for i in range(1, count + 1):
        message = {
            'id': i,
            'content': f'Message {i}',
            'priority': priorities[i % 3]
        }
        messages.append(message)

    return messages


def main():
    buffer_capacity = 5
    message_count = 20

    print(f"--- Producer-Consumer Pattern Demo ---")
    print(f"Buffer capacity: {buffer_capacity}")
    print(f"Total messages: {message_count}\n")

    shared_buffer = SharedBuffer(capacity=buffer_capacity)
    messages = create_messages(message_count)

    producer = Producer(shared_buffer, messages)
    consumer = Consumer(shared_buffer)

    producer_thread = threading.Thread(target=producer.run, name="ProducerThread")
    consumer_thread = threading.Thread(target=consumer.run, name="ConsumerThread")

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    print(f"\n--- Execution Summary ---")
    print(f"Items produced: {producer.items_produced}")
    print(f"Items consumed: {consumer.items_consumed}")
    print(f"Remaining in buffer: {shared_buffer.size()}")
    print(f"Verification: {'✓ Success' if producer.items_produced == consumer.items_consumed else '✗ Failed'}")


if __name__ == "__main__":
    main()
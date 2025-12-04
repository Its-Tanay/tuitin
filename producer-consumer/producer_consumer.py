import threading
import time


class ProducerConsumer:
    def __init__(self, buffer_size):
        self.source = []
        self.buffer = []
        self.destination = []
        self.buffer_size = buffer_size
        self.producer_done = False
        self.condition = threading.Condition()

    def produce(self):
        while len(self.source) > 0:
            with self.condition:
                while len(self.buffer) >= self.buffer_size:
                    print("Buffer full, producer waiting...")
                    self.condition.wait()

                item = self.source.pop(0)
                self.buffer.append(item)
                print(f"Produced: {item['id']} - Buffer size: {len(self.buffer)}")
                self.condition.notify()

            time.sleep(0.1)

        with self.condition:
            self.producer_done = True
            self.condition.notify()

        print("Producer finished")

    def consume(self):
        while True:
            with self.condition:
                while len(self.buffer) == 0 and not self.producer_done:
                    print("Buffer empty, consumer waiting...")
                    self.condition.wait()

                if len(self.buffer) == 0 and self.producer_done:
                    break

                item = self.buffer.pop(0)
                self.destination.append(item)
                print(f"Consumed: {item['id']} - Buffer size: {len(self.buffer)}")
                self.condition.notify()

            time.sleep(0.15)

        print("Consumer finished")


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
    pc = ProducerConsumer(buffer_size=5)
    pc.source = create_messages(20)

    print(f"Starting with {len(pc.source)} messages in source")
    print(f"Buffer capacity: {pc.buffer_size}\n")

    producer_thread = threading.Thread(target=pc.produce, name="Producer")
    consumer_thread = threading.Thread(target=pc.consume, name="Consumer")

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    print(f"\nCompleted!")
    print(f"Source: {len(pc.source)} items")
    print(f"Buffer: {len(pc.buffer)} items")
    print(f"Destination: {len(pc.destination)} items")


if __name__ == "__main__":
    main()
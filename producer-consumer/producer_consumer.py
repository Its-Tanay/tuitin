import threading
import time


class ProducerConsumer:
    def __init__(self, buffer_size):
        self.source = []
        self.buffer = []
        self.destination = []
        self.buffer_size = buffer_size
        self.producer_done = False

    def produce(self):
        while len(self.source) > 0:
            if len(self.buffer) < self.buffer_size:
                item = self.source.pop(0)
                self.buffer.append(item)
                print(f"Produced: {item['id']} - Buffer size: {len(self.buffer)}")
                time.sleep(0.1)
            else:
                print("Buffer full, producer waiting...")
                time.sleep(0.1)

        self.producer_done = True
        print("Producer finished")

    def consume(self):
        while not self.producer_done or len(self.buffer) > 0:
            if len(self.buffer) > 0:
                item = self.buffer.pop(0)
                self.destination.append(item)
                print(f"Consumed: {item['id']} - Buffer size: {len(self.buffer)}")
                time.sleep(0.15)
            else:
                print("Buffer empty, consumer waiting...")
                time.sleep(0.1)

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
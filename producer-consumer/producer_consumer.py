class ProducerConsumer:
    def __init__(self, buffer_size):
        self.source = []
        self.buffer = []
        self.destination = []
        self.buffer_size = buffer_size
        self.is_done = False

    def produce(self):
        while len(self.source) > 0:
            if len(self.buffer) < self.buffer_size:
                item = self.source.pop(0)
                self.buffer.append(item)
                print(f"Produced: {item['id']} - Buffer size: {len(self.buffer)}")
            else:
                print("Buffer full, waiting...")
                break

        if len(self.source) == 0:
            self.is_done = True

    def consume(self):
        while len(self.buffer) > 0:
            item = self.buffer.pop(0)
            self.destination.append(item)
            print(f"Consumed: {item['id']} - Buffer size: {len(self.buffer)}")

        if len(self.buffer) == 0 and not self.is_done:
            print("Buffer empty, waiting...")


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

    while not pc.is_done or len(pc.buffer) > 0:
        pc.produce()
        pc.consume()

    print(f"\nCompleted!")
    print(f"Source: {len(pc.source)} items")
    print(f"Buffer: {len(pc.buffer)} items")
    print(f"Destination: {len(pc.destination)} items")


if __name__ == "__main__":
    main()
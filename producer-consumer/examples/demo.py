import sys
sys.path.insert(0, '..')

from main import ProducerConsumerPipeline


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


def on_produce(item, count, buffer_size):
    print(f"[Producer] Message {item['id']} produced | Buffer: {buffer_size}")


def on_consume(item, count, buffer_size):
    print(f"[Consumer] Message {item['id']} consumed | Buffer: {buffer_size}")


def main():
    print("--- Producer-Consumer Pattern Demo ---\n")

    pipeline = ProducerConsumerPipeline(buffer_capacity=5)
    messages = create_messages(20)

    results = pipeline.process(
        messages,
        producer_delay=0.1,
        consumer_delay=0.15,
        on_produce=on_produce,
        on_consume=on_consume
    )

    stats = pipeline.get_stats()

    print(f"\n--- Execution Summary ---")
    print(f"Messages processed: {len(results)}")
    print(f"Items produced: {stats['produced']}")
    print(f"Items consumed: {stats['consumed']}")
    print(f"Verification: {'✓ Success' if stats['success'] else '✗ Failed'}")


if __name__ == "__main__":
    main()
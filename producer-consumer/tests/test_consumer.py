import unittest
import threading
import sys
sys.path.insert(0, '..')

from src.buffer import SharedBuffer
from src.consumer import Consumer


class TestConsumer(unittest.TestCase):

    def test_consumer_initialization(self):
        buffer = SharedBuffer(capacity=5)
        consumer = Consumer(buffer)

        self.assertEqual(consumer.items_consumed, 0)
        self.assertEqual(len(consumer.consumed_items), 0)
        self.assertEqual(consumer.delay, 0)

    def test_consumer_processes_single_item(self):
        buffer = SharedBuffer(capacity=5)
        buffer.put(42)
        buffer.mark_complete()

        consumer = Consumer(buffer)
        consumer.run()

        self.assertEqual(consumer.items_consumed, 1)
        self.assertEqual(consumer.consumed_items, [42])

    def test_consumer_processes_multiple_items(self):
        buffer = SharedBuffer(capacity=5)
        items = [1, 2, 3, 4, 5]

        for item in items:
            buffer.put(item)
        buffer.mark_complete()

        consumer = Consumer(buffer)
        consumer.run()

        self.assertEqual(consumer.items_consumed, 5)
        self.assertEqual(consumer.consumed_items, items)

    def test_consumer_with_empty_buffer(self):
        buffer = SharedBuffer(capacity=5)
        buffer.mark_complete()

        consumer = Consumer(buffer)
        consumer.run()

        self.assertEqual(consumer.items_consumed, 0)
        self.assertEqual(consumer.consumed_items, [])

    def test_consumer_with_callback(self):
        buffer = SharedBuffer(capacity=5)
        items = [1, 2, 3]
        callback_data = []

        def callback(item, count, buffer_size):
            callback_data.append({
                'item': item,
                'count': count,
                'buffer_size': buffer_size
            })

        for item in items:
            buffer.put(item)
        buffer.mark_complete()

        consumer = Consumer(buffer, on_consume=callback)
        consumer.run()

        self.assertEqual(len(callback_data), 3)
        self.assertEqual(callback_data[0]['item'], 1)
        self.assertEqual(callback_data[0]['count'], 1)
        self.assertEqual(callback_data[2]['count'], 3)

    def test_consumer_with_delay(self):
        buffer = SharedBuffer(capacity=5)
        buffer.put(1)
        buffer.put(2)
        buffer.mark_complete()

        consumer = Consumer(buffer, delay=0.05)

        import time
        start = time.time()
        consumer.run()
        duration = time.time() - start

        self.assertGreaterEqual(duration, 0.1)
        self.assertEqual(consumer.items_consumed, 2)

    def test_consumer_waits_for_producer(self):
        buffer = SharedBuffer(capacity=5)
        consumer = Consumer(buffer)

        def delayed_producer():
            import time
            time.sleep(0.1)
            buffer.put(99)
            buffer.mark_complete()

        producer_thread = threading.Thread(target=delayed_producer)
        consumer_thread = threading.Thread(target=consumer.run)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        self.assertEqual(consumer.items_consumed, 1)
        self.assertEqual(consumer.consumed_items, [99])

    def test_consumer_without_callback(self):
        buffer = SharedBuffer(capacity=5)
        buffer.put(1)
        buffer.put(2)
        buffer.mark_complete()

        consumer = Consumer(buffer, on_consume=None)
        consumer.run()

        self.assertEqual(consumer.items_consumed, 2)

    def test_consumer_with_dict_items(self):
        buffer = SharedBuffer(capacity=5)
        items = [
            {'id': 1, 'value': 'a'},
            {'id': 2, 'value': 'b'}
        ]

        for item in items:
            buffer.put(item)
        buffer.mark_complete()

        consumer = Consumer(buffer)
        consumer.run()

        self.assertEqual(consumer.consumed_items, items)

    def test_consumer_callback_receives_correct_buffer_size(self):
        buffer = SharedBuffer(capacity=5)
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)
        buffer.mark_complete()

        buffer_sizes = []

        def callback(item, count, buffer_size):
            buffer_sizes.append(buffer_size)

        consumer = Consumer(buffer, on_consume=callback)
        consumer.run()

        self.assertEqual(buffer_sizes, [2, 1, 0])

    def test_consumer_stops_when_buffer_empty_and_complete(self):
        buffer = SharedBuffer(capacity=5)
        buffer.put(1)
        buffer.mark_complete()

        consumer = Consumer(buffer)
        consumer.run()

        self.assertEqual(consumer.items_consumed, 1)

    def test_consumer_processes_large_dataset(self):
        buffer = SharedBuffer(capacity=10)
        items = list(range(100))

        def producer_thread():
            for item in items:
                buffer.put(item)
            buffer.mark_complete()

        consumer = Consumer(buffer)

        producer = threading.Thread(target=producer_thread)
        consumer_thread = threading.Thread(target=consumer.run)

        producer.start()
        consumer_thread.start()

        producer.join()
        consumer_thread.join()

        self.assertEqual(consumer.items_consumed, 100)
        self.assertEqual(sorted(consumer.consumed_items), items)


if __name__ == '__main__':
    unittest.main()
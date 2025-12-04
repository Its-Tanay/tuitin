import unittest
import threading
import sys
sys.path.insert(0, '..')

from src.buffer import SharedBuffer
from src.producer import Producer

class TestProducer(unittest.TestCase):

    def test_producer_initialization(self):
        buffer = SharedBuffer(capacity=5)
        data = [1, 2, 3]
        producer = Producer(buffer, data)

        self.assertEqual(producer.source_data, data)
        self.assertEqual(producer.items_produced, 0)
        self.assertEqual(producer.delay, 0)

    def test_producer_with_empty_data(self):
        buffer = SharedBuffer(capacity=5)
        producer = Producer(buffer, [])

        producer.run()

        self.assertEqual(producer.items_produced, 0)
        self.assertTrue(buffer.production_complete)

    def test_producer_processes_all_items(self):
        buffer = SharedBuffer(capacity=10)
        data = [1, 2, 3, 4, 5]
        producer = Producer(buffer, data)

        producer.run()

        self.assertEqual(producer.items_produced, 5)
        self.assertEqual(buffer.size(), 5)
        self.assertTrue(buffer.production_complete)

    def test_producer_with_callback(self):
        buffer = SharedBuffer(capacity=5)
        data = [1, 2, 3]
        callback_data = []

        def callback(item, count, buffer_size):
            callback_data.append({
                'item': item,
                'count': count,
                'buffer_size': buffer_size
            })

        producer = Producer(buffer, data, on_produce=callback)
        producer.run()

        self.assertEqual(len(callback_data), 3)
        self.assertEqual(callback_data[0]['item'], 1)
        self.assertEqual(callback_data[0]['count'], 1)
        self.assertEqual(callback_data[2]['count'], 3)

    def test_producer_with_delay(self):
        buffer = SharedBuffer(capacity=5)
        data = [1, 2]
        producer = Producer(buffer, data, delay=0.05)

        import time
        start = time.time()
        producer.run()
        duration = time.time() - start

        self.assertGreaterEqual(duration, 0.1)
        self.assertEqual(producer.items_produced, 2)

    def test_producer_marks_buffer_complete(self):
        buffer = SharedBuffer(capacity=5)
        data = [1, 2, 3]
        producer = Producer(buffer, data)

        self.assertFalse(buffer.production_complete)
        producer.run()
        self.assertTrue(buffer.production_complete)

    def test_producer_with_single_item(self):
        buffer = SharedBuffer(capacity=5)
        data = [42]
        producer = Producer(buffer, data)

        producer.run()

        self.assertEqual(producer.items_produced, 1)
        self.assertEqual(buffer.get(), 42)

    def test_producer_with_large_dataset(self):
        buffer = SharedBuffer(capacity=10)
        data = list(range(100))
        producer = Producer(buffer, data)

        def consumer_thread():
            while True:
                item = buffer.get()
                if item is None:
                    break

        consumer = threading.Thread(target=consumer_thread)
        consumer.start()

        producer.run()
        consumer.join()

        self.assertEqual(producer.items_produced, 100)

    def test_producer_with_dict_items(self):
        buffer = SharedBuffer(capacity=5)
        data = [
            {'id': 1, 'value': 'a'},
            {'id': 2, 'value': 'b'},
            {'id': 3, 'value': 'c'}
        ]
        producer = Producer(buffer, data)

        producer.run()

        self.assertEqual(producer.items_produced, 3)
        self.assertEqual(buffer.get(), {'id': 1, 'value': 'a'})

    def test_producer_callback_receives_correct_buffer_size(self):
        buffer = SharedBuffer(capacity=5)
        data = [1, 2, 3]
        buffer_sizes = []

        def callback(item, count, buffer_size):
            buffer_sizes.append(buffer_size)

        producer = Producer(buffer, data, on_produce=callback)
        producer.run()

        self.assertEqual(buffer_sizes, [1, 2, 3])

    def test_producer_without_callback(self):
        buffer = SharedBuffer(capacity=5)
        data = [1, 2, 3]
        producer = Producer(buffer, data, on_produce=None)

        producer.run()

        self.assertEqual(producer.items_produced, 3)

if __name__ == '__main__':
    unittest.main()

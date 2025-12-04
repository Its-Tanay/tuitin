import unittest
import threading
import time
import sys
sys.path.insert(0, '..')

from src.buffer import SharedBuffer

class TestSharedBuffer(unittest.TestCase):

    def test_buffer_initialization(self):
        buffer = SharedBuffer(capacity=5)
        self.assertEqual(buffer.capacity, 5)
        self.assertEqual(buffer.size(), 0)
        self.assertFalse(buffer.production_complete)

    def test_put_single_item(self):
        buffer = SharedBuffer(capacity=5)
        buffer.put(1)
        self.assertEqual(buffer.size(), 1)

    def test_get_single_item(self):
        buffer = SharedBuffer(capacity=5)
        buffer.put(42)
        item = buffer.get()
        self.assertEqual(item, 42)
        self.assertEqual(buffer.size(), 0)

    def test_fifo_order(self):
        buffer = SharedBuffer(capacity=5)
        items = [1, 2, 3, 4, 5]

        for item in items:
            buffer.put(item)

        result = []
        buffer.mark_complete()
        for _ in range(5):
            result.append(buffer.get())

        self.assertEqual(result, items)

    def test_capacity_limit(self):
        buffer = SharedBuffer(capacity=3)
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)
        self.assertEqual(buffer.size(), 3)

    def test_get_returns_none_when_complete_and_empty(self):
        buffer = SharedBuffer(capacity=5)
        buffer.mark_complete()
        item = buffer.get()
        self.assertIsNone(item)

    def test_mark_complete(self):
        buffer = SharedBuffer(capacity=5)
        self.assertFalse(buffer.production_complete)
        buffer.mark_complete()
        self.assertTrue(buffer.production_complete)

    def test_blocking_put_when_full(self):
        buffer = SharedBuffer(capacity=2)
        buffer.put(1)
        buffer.put(2)

        put_completed = [False]

        def try_put():
            buffer.put(3)
            put_completed[0] = True

        thread = threading.Thread(target=try_put)
        thread.start()

        time.sleep(0.1)
        self.assertFalse(put_completed[0])

        buffer.get()
        thread.join(timeout=1)
        self.assertTrue(put_completed[0])

    def test_blocking_get_when_empty(self):
        buffer = SharedBuffer(capacity=5)

        get_result = [None]

        def try_get():
            get_result[0] = buffer.get()

        thread = threading.Thread(target=try_get)
        thread.start()

        time.sleep(0.1)
        self.assertTrue(thread.is_alive())

        buffer.put(99)
        thread.join(timeout=1)
        self.assertEqual(get_result[0], 99)

    def test_concurrent_put_get(self):
        buffer = SharedBuffer(capacity=10)
        items_to_process = 100

        def producer():
            for i in range(items_to_process):
                buffer.put(i)
            buffer.mark_complete()

        def consumer(result_list):
            while True:
                item = buffer.get()
                if item is None:
                    break
                result_list.append(item)

        results = []
        p_thread = threading.Thread(target=producer)
        c_thread = threading.Thread(target=consumer, args=(results,))

        p_thread.start()
        c_thread.start()

        p_thread.join()
        c_thread.join()

        self.assertEqual(len(results), items_to_process)
        self.assertEqual(sorted(results), list(range(items_to_process)))

    def test_multiple_consumers(self):
        buffer = SharedBuffer(capacity=10)
        items_to_process = 50

        def producer():
            for i in range(items_to_process):
                buffer.put(i)
            buffer.mark_complete()

        def consumer(result_list):
            while True:
                item = buffer.get()
                if item is None:
                    break
                result_list.append(item)

        results1 = []
        results2 = []

        p_thread = threading.Thread(target=producer)
        c1_thread = threading.Thread(target=consumer, args=(results1,))
        c2_thread = threading.Thread(target=consumer, args=(results2,))

        p_thread.start()
        c1_thread.start()
        c2_thread.start()

        p_thread.join()
        c1_thread.join()
        c2_thread.join()

        all_results = results1 + results2
        self.assertEqual(len(all_results), items_to_process)
        self.assertEqual(sorted(all_results), list(range(items_to_process)))

    def test_empty_buffer_size(self):
        buffer = SharedBuffer(capacity=10)
        self.assertEqual(buffer.size(), 0)

    def test_buffer_with_different_types(self):
        buffer = SharedBuffer(capacity=5)

        buffer.put(42)
        buffer.put("string")
        buffer.put({'key': 'value'})
        buffer.put([1, 2, 3])
        buffer.put((1, 2))

        self.assertEqual(buffer.get(), 42)
        self.assertEqual(buffer.get(), "string")
        self.assertEqual(buffer.get(), {'key': 'value'})
        self.assertEqual(buffer.get(), [1, 2, 3])
        self.assertEqual(buffer.get(), (1, 2))

if __name__ == '__main__':
    unittest.main()

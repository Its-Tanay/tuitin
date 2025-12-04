import unittest
import sys
sys.path.insert(0, '..')

from src.pipeline import ProducerConsumerPipeline


class TestProducerConsumerPipeline(unittest.TestCase):

    def test_pipeline_initialization(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        self.assertEqual(pipeline.buffer_capacity, 5)
        self.assertIsNone(pipeline.shared_buffer)
        self.assertIsNone(pipeline.producer)
        self.assertIsNone(pipeline.consumer)

    def test_pipeline_processes_simple_data(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=10)
        data = [1, 2, 3, 4, 5]

        results = pipeline.process(data)

        self.assertEqual(results, data)
        self.assertEqual(len(results), 5)

    def test_pipeline_with_empty_data(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = []

        results = pipeline.process(data)

        self.assertEqual(results, [])
        self.assertEqual(len(results), 0)

    def test_pipeline_get_stats(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = [1, 2, 3, 4, 5]

        pipeline.process(data)
        stats = pipeline.get_stats()

        self.assertEqual(stats['produced'], 5)
        self.assertEqual(stats['consumed'], 5)
        self.assertTrue(stats['success'])

    def test_pipeline_get_stats_before_processing(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        stats = pipeline.get_stats()

        self.assertIsNone(stats)

    def test_pipeline_with_large_dataset(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=10)
        data = list(range(100))

        results = pipeline.process(data)

        self.assertEqual(len(results), 100)
        self.assertEqual(sorted(results), data)

    def test_pipeline_with_small_buffer(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=2)
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        results = pipeline.process(data)

        self.assertEqual(len(results), 10)
        self.assertEqual(results, data)

    def test_pipeline_with_delays(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = [1, 2, 3]

        results = pipeline.process(
            data,
            producer_delay=0.01,
            consumer_delay=0.01
        )

        self.assertEqual(results, data)

    def test_pipeline_with_callbacks(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = [1, 2, 3]

        produced_items = []
        consumed_items = []

        def on_produce(item, count, buffer_size):
            produced_items.append(item)

        def on_consume(item, count, buffer_size):
            consumed_items.append(item)

        results = pipeline.process(
            data,
            on_produce=on_produce,
            on_consume=on_consume
        )

        self.assertEqual(produced_items, data)
        self.assertEqual(consumed_items, data)
        self.assertEqual(results, data)

    def test_pipeline_with_dict_data(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = [
            {'id': 1, 'value': 'a'},
            {'id': 2, 'value': 'b'},
            {'id': 3, 'value': 'c'}
        ]

        results = pipeline.process(data)

        self.assertEqual(results, data)

    def test_pipeline_with_mixed_types(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = [1, "string", {'key': 'value'}, [1, 2, 3], (1, 2)]

        results = pipeline.process(data)

        self.assertEqual(results, data)

    def test_pipeline_maintains_order(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = list(range(50))

        results = pipeline.process(data)

        self.assertEqual(results, data)

    def test_pipeline_with_single_item(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = [42]

        results = pipeline.process(data)

        self.assertEqual(results, [42])

    def test_pipeline_buffer_never_exceeds_capacity(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = list(range(20))

        max_buffer_size = [0]

        def on_produce(item, count, buffer_size):
            max_buffer_size[0] = max(max_buffer_size[0], buffer_size)

        pipeline.process(data, on_produce=on_produce)

        self.assertLessEqual(max_buffer_size[0], 5)

    def test_pipeline_stats_success_flag(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = list(range(10))

        pipeline.process(data)
        stats = pipeline.get_stats()

        self.assertTrue(stats['success'])
        self.assertEqual(stats['produced'], stats['consumed'])

    def test_pipeline_multiple_runs(self):
        pipeline1 = ProducerConsumerPipeline(buffer_capacity=5)
        data1 = [1, 2, 3]
        results1 = pipeline1.process(data1)

        pipeline2 = ProducerConsumerPipeline(buffer_capacity=5)
        data2 = [4, 5, 6]
        results2 = pipeline2.process(data2)

        self.assertEqual(results1, data1)
        self.assertEqual(results2, data2)

    def test_pipeline_with_callback_counts(self):
        pipeline = ProducerConsumerPipeline(buffer_capacity=5)
        data = [1, 2, 3]

        produce_counts = []
        consume_counts = []

        def on_produce(item, count, buffer_size):
            produce_counts.append(count)

        def on_consume(item, count, buffer_size):
            consume_counts.append(count)

        pipeline.process(
            data,
            on_produce=on_produce,
            on_consume=on_consume
        )

        self.assertEqual(produce_counts, [1, 2, 3])
        self.assertEqual(consume_counts, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
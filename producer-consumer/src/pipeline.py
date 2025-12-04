import threading
from .buffer import SharedBuffer
from .producer import Producer
from .consumer import Consumer


class ProducerConsumerPipeline:
    """
    High-level orchestrator for producer-consumer pattern execution.

    This class provides a simple interface to run producer-consumer operations
    without manually managing threads or synchronization. It handles thread
    creation, execution, and cleanup automatically.
    """

    def __init__(self, buffer_capacity=10):
        """
        Initialize the pipeline with buffer configuration.

        Args:
            buffer_capacity: Maximum number of items the buffer can hold (default: 10)
        """
        self.buffer_capacity = buffer_capacity

        # These will be initialized when process is called
        self.shared_buffer = None
        self.producer = None
        self.consumer = None
        self.producer_thread = None
        self.consumer_thread = None

    def process(self, data, producer_delay=0, consumer_delay=0,
                on_produce=None, on_consume=None):
        """
        Execute the producer-consumer pipeline with the given data.

        Creates a shared buffer, producer, and consumer, then runs them
        concurrently in separate threads. Blocks until all data is processed.

        Args:
            data: List of items to process through the pipeline
            producer_delay: Optional delay between producing items (default: 0)
            consumer_delay: Optional delay between consuming items (default: 0)
            on_produce: Optional callback function(item, count, buffer_size)
                       called after each item is produced
            on_consume: Optional callback function(item, count, buffer_size)
                       called after each item is consumed

        Returns:
            List of all consumed items in order
        """
        # Create shared buffer for communication
        self.shared_buffer = SharedBuffer(capacity=self.buffer_capacity)

        # Create producer with source data
        self.producer = Producer(
            self.shared_buffer,
            data,
            delay=producer_delay,
            on_produce=on_produce
        )

        # Create consumer to process items
        self.consumer = Consumer(
            self.shared_buffer,
            delay=consumer_delay,
            on_consume=on_consume
        )

        # Create threads for concurrent execution
        self.producer_thread = threading.Thread(target=self.producer.run)
        self.consumer_thread = threading.Thread(target=self.consumer.run)

        # Start both threads
        self.producer_thread.start()
        self.consumer_thread.start()

        # Wait for both threads to complete
        self.producer_thread.join()
        self.consumer_thread.join()

        # Return all consumed items
        return self.consumer.consumed_items

    def get_stats(self):
        """
        Get statistics about the last pipeline execution.

        Returns a dictionary with production and consumption counts,
        and a success flag indicating if all items were processed.

        Returns:
            Dictionary with 'produced', 'consumed', and 'success' keys,
            or None if process has not been called yet
        """
        if not self.producer or not self.consumer:
            return None

        return {
            'produced': self.producer.items_produced,
            'consumed': self.consumer.items_consumed,
            'success': self.producer.items_produced == self.consumer.items_consumed
        }
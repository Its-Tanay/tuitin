import threading
from .buffer import SharedBuffer
from .producer import Producer
from .consumer import Consumer

class ProducerConsumerPipeline:
    def __init__(self, buffer_capacity=10):
        self.buffer_capacity = buffer_capacity
        self.shared_buffer = None
        self.producer = None
        self.consumer = None
        self.producer_thread = None
        self.consumer_thread = None

    def process(self, data, producer_delay=0, consumer_delay=0,
                on_produce=None, on_consume=None):
        self.shared_buffer = SharedBuffer(capacity=self.buffer_capacity)

        self.producer = Producer(
            self.shared_buffer,
            data,
            delay=producer_delay,
            on_produce=on_produce
        )

        self.consumer = Consumer(
            self.shared_buffer,
            delay=consumer_delay,
            on_consume=on_consume
        )

        self.producer_thread = threading.Thread(target=self.producer.run)
        self.consumer_thread = threading.Thread(target=self.consumer.run)

        self.producer_thread.start()
        self.consumer_thread.start()

        self.producer_thread.join()
        self.consumer_thread.join()

        return self.consumer.consumed_items

    def get_stats(self):
        if not self.producer or not self.consumer:
            return None

        return {
            'produced': self.producer.items_produced,
            'consumed': self.consumer.items_consumed,
            'success': self.producer.items_produced == self.consumer.items_consumed
        }
    
import time


class Consumer:
    """
    Consumer that retrieves items from a shared buffer and processes them.

    The consumer continuously reads items from the buffer until production is complete
    and the buffer is empty. It stores all consumed items and can optionally invoke
    a callback after each consumption.
    """

    def __init__(self, shared_buffer, delay=0, on_consume=None):
        """
        Initialize the consumer with buffer reference and configuration.

        Args:
            shared_buffer: The SharedBuffer instance to consume from
            delay: Optional delay in seconds between consuming items (default: 0)
            on_consume: Optional callback function(item, count, buffer_size)
                       called after each item is consumed
        """
        self.shared_buffer = shared_buffer
        self.delay = delay
        self.on_consume = on_consume

        # Store all consumed items in order
        self.consumed_items = []

        # Track how many items have been consumed
        self.items_consumed = 0

    def run(self):
        """
        Execute the consumer loop.

        Continuously retrieves items from the buffer until None is returned,
        which signals that production is complete and buffer is empty.
        Calls the callback if provided and applies delay if configured.
        """
        while True:
            # Get next item from buffer, blocks if empty
            item = self.shared_buffer.get()

            # None signals end of production
            if item is None:
                break

            # Store item and update counter
            self.consumed_items.append(item)
            self.items_consumed += 1

            # Call user-provided callback if present
            if self.on_consume:
                self.on_consume(item, self.items_consumed, self.shared_buffer.size())

            # Apply delay between items if configured
            if self.delay > 0:
                time.sleep(self.delay)
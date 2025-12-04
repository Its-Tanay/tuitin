import time


class Producer:
    """
    Producer that reads items from source data and places them into a shared buffer.

    The producer iterates through source data and adds each item to the buffer.
    It can optionally delay between items and invoke a callback after each production.
    """

    def __init__(self, shared_buffer, source_data, delay=0, on_produce=None):
        """
        Initialize the producer with data source and configuration.

        Args:
            shared_buffer: The SharedBuffer instance to produce into
            source_data: List of items to produce
            delay: Optional delay in seconds between producing items (default: 0)
            on_produce: Optional callback function(item, count, buffer_size)
                       called after each item is produced
        """
        self.shared_buffer = shared_buffer
        self.source_data = source_data
        self.delay = delay
        self.on_produce = on_produce

        # Track how many items have been produced
        self.items_produced = 0

    def run(self):
        """
        Execute the producer loop.

        Iterates through source data, adding each item to the buffer.
        Calls the callback if provided and applies delay if configured.
        Marks the buffer as complete when all items are produced.
        """
        for item in self.source_data:
            # Add item to the shared buffer
            self.shared_buffer.put(item)
            self.items_produced += 1

            # Call user-provided callback if present
            if self.on_produce:
                self.on_produce(item, self.items_produced, self.shared_buffer.size())

            # Apply delay between items if configured
            if self.delay > 0:
                time.sleep(self.delay)

        # Signal that no more items will be produced
        self.shared_buffer.mark_complete()
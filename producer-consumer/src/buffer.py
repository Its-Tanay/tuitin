import threading


class SharedBuffer:
    """
    Thread-safe buffer for producer-consumer communication.

    This buffer uses a Condition variable to coordinate access between
    multiple producer and consumer threads. It blocks producers when full
    and consumers when empty, implementing classic wait/notify patterns.
    """

    def __init__(self, capacity):
        """
        Initialize the shared buffer with a fixed capacity.

        Args:
            capacity: Maximum number of items the buffer can hold
        """
        self.capacity = capacity
        self.buffer = []

        # Condition variable for thread synchronization
        self.condition = threading.Condition()

        # Flag to signal when production is complete
        self.production_complete = False

    def put(self, item):
        """
        Add an item to the buffer. Blocks if buffer is at capacity.

        This method will wait until there is space in the buffer before
        adding the item. It notifies waiting consumers after adding.

        Args:
            item: The item to add to the buffer
        """
        with self.condition:
            # Wait while buffer is full
            while len(self.buffer) >= self.capacity:
                self.condition.wait()

            # Add item and notify any waiting consumers
            self.buffer.append(item)
            self.condition.notify()

    def get(self):
        """
        Remove and return an item from the buffer. Blocks if buffer is empty.

        This method waits until an item is available or production is complete.
        Returns None if buffer is empty and production has finished.

        Returns:
            The next item from the buffer, or None if production is complete
        """
        with self.condition:
            # Wait while buffer is empty and production is ongoing
            while len(self.buffer) == 0 and not self.production_complete:
                self.condition.wait()

            # Return None if buffer is empty and production is done
            if len(self.buffer) == 0:
                return None

            # Remove item from front and notify any waiting producers
            item = self.buffer.pop(0)
            self.condition.notify()
            return item

    def mark_complete(self):
        """
        Signal that production is complete.

        This notifies all waiting consumers that no more items will be added.
        Consumers can then finish processing remaining items and exit.
        """
        with self.condition:
            self.production_complete = True
            self.condition.notify()

    def size(self):
        """
        Get the current number of items in the buffer.

        Returns:
            Current buffer size
        """
        return len(self.buffer)
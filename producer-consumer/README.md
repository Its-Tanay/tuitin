# Producer-Consumer Pattern Implementation

A thread-safe implementation of the classic producer-consumer pattern in Python, demonstrating concurrent programming with proper synchronization using threading primitives.

## Features

- Thread-safe shared buffer with blocking operations
- Producer and consumer components with configurable delays
- Support for custom callbacks during production and consumption
- High-level pipeline API for easy integration
- Comprehensive test coverage with 53 unit tests
- Well-documented codebase

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Setup Instructions

### 1. Clone or navigate to the project directory

```bash
cd producer-consumer
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Verify installation

```bash
python3 main.py
```

## Usage

### Basic Usage

```python
from main import ProducerConsumerPipeline

# Create pipeline with buffer capacity of 5
pipeline = ProducerConsumerPipeline(buffer_capacity=5)

# Process data
data = [1, 2, 3, 4, 5]
results = pipeline.process(data)

print(f"Processed: {results}")
```

### Advanced Usage with Callbacks

```python
from main import ProducerConsumerPipeline

def on_produce(item, count, buffer_size):
    print(f"Produced: {item} | Buffer: {buffer_size}")

def on_consume(item, count, buffer_size):
    print(f"Consumed: {item} | Buffer: {buffer_size}")

pipeline = ProducerConsumerPipeline(buffer_capacity=5)

messages = [
    {'id': 1, 'content': 'Message 1'},
    {'id': 2, 'content': 'Message 2'},
    {'id': 3, 'content': 'Message 3'}
]

results = pipeline.process(
    messages,
    producer_delay=0.1,
    consumer_delay=0.15,
    on_produce=on_produce,
    on_consume=on_consume
)

stats = pipeline.get_stats()
print(f"Items produced: {stats['produced']}")
print(f"Items consumed: {stats['consumed']}")
print(f"Success: {stats['success']}")
```

## Sample Output

Running the demo file:

```bash
python3 examples/demo.py
```

```
--- Producer-Consumer Pattern Demo ---
Buffer capacity: 5
Total messages: 20

[Producer] Message 1 produced | Buffer: 1
[Consumer] Message 1 consumed | Buffer: 0
[Producer] Message 2 produced | Buffer: 1
[Consumer] Message 2 consumed | Buffer: 0
[Producer] Message 3 produced | Buffer: 1
[Consumer] Message 3 consumed | Buffer: 0
[Producer] Message 4 produced | Buffer: 1
[Producer] Message 5 produced | Buffer: 2
[Consumer] Message 4 consumed | Buffer: 1
...

--- Execution Summary ---
Messages processed: 20
Items produced: 20
Items consumed: 20
Verification: Success
```

## Running Tests

The project includes comprehensive unit tests covering all components and edge cases.

### Run all tests

```bash
python3 -m unittest discover tests -v
```

### Run specific test file

```bash
python3 -m unittest tests.test_buffer -v
python3 -m unittest tests.test_producer -v
python3 -m unittest tests.test_consumer -v
python3 -m unittest tests.test_pipeline -v
```

### Expected test output

```
----------------------------------------------------------------------
Ran 53 tests in 0.582s

OK
```

## Project Structure

```
producer-consumer/
├── main.py                    # Public API entry point
├── src/                       # Core implementation
│   ├── __init__.py
│   ├── buffer.py             # Thread-safe shared buffer
│   ├── consumer.py           # Consumer component
│   ├── producer.py           # Producer component
│   └── pipeline.py           # High-level orchestrator
├── tests/                     # Unit tests
│   ├── __init__.py
│   ├── test_buffer.py        # Buffer tests (13 tests)
│   ├── test_consumer.py      # Consumer tests (12 tests)
│   ├── test_producer.py      # Producer tests (11 tests)
│   └── test_pipeline.py      # Pipeline tests (17 tests)
├── examples/
│   └── demo.py               # Usage demonstration
└── README.md                  # This file
```

## Technical Details

### Thread Synchronization

The implementation uses Python's `threading.Condition` for synchronization:

- Producers block when the buffer is full
- Consumers block when the buffer is empty
- Proper wait/notify mechanism prevents race conditions
- Thread-safe operations on shared data structures

### Design Pattern

The implementation follows the classic producer-consumer pattern:

1. **SharedBuffer**: Thread-safe queue with capacity limits
2. **Producer**: Reads from source and adds to buffer
3. **Consumer**: Reads from buffer and processes items
4. **ProducerConsumerPipeline**: Orchestrates the entire flow

## API Reference

### ProducerConsumerPipeline

Main interface for using the producer-consumer pattern.

**Methods:**
- `__init__(buffer_capacity=10)`: Initialize with buffer size
- `process(data, producer_delay=0, consumer_delay=0, on_produce=None, on_consume=None)`: Process data through pipeline
- `get_stats()`: Get execution statistics

### SharedBuffer

Thread-safe buffer for producer-consumer communication.

**Methods:**
- `put(item)`: Add item to buffer (blocks if full)
- `get()`: Remove item from buffer (blocks if empty)
- `mark_complete()`: Signal production is complete
- `size()`: Get current buffer size

### Producer

Component that produces items into the buffer.

**Methods:**
- `__init__(shared_buffer, source_data, delay=0, on_produce=None)`: Initialize producer
- `run()`: Execute production loop

### Consumer

Component that consumes items from the buffer.

**Methods:**
- `__init__(shared_buffer, delay=0, on_consume=None)`: Initialize consumer
- `run()`: Execute consumption loop

## Cases Covered

- Thread synchronization with Condition variables
- Concurrent programming with multiple threads
- Blocking queue behavior
- Wait/Notify mechanism
- Edge cases: empty data, large datasets, small buffers
- FIFO ordering preservation
- Multiple consumers scenario
"""
Producer-Consumer Pattern Implementation

This module provides a thread-safe implementation of the classic producer-consumer
pattern using Python's threading primitives. It includes:

- ProducerConsumerPipeline: High-level API for easy usage
- SharedBuffer: Thread-safe buffer with blocking operations
- Producer: Component that produces items into the buffer
- Consumer: Component that consumes items from the buffer

Usage:
    from main import ProducerConsumerPipeline

    pipeline = ProducerConsumerPipeline(buffer_capacity=5)
    data = [1, 2, 3, 4, 5]
    results = pipeline.process(data)
"""

from src.pipeline import ProducerConsumerPipeline
from src.buffer import SharedBuffer
from src.producer import Producer
from src.consumer import Consumer

__all__ = [
    'ProducerConsumerPipeline',
    'SharedBuffer',
    'Producer',
    'Consumer'
]
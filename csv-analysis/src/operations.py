"""
Functional programming operations for data processing.

This module provides pure functional operations demonstrating
filter, map, reduce, and aggregation patterns with lambda expressions.
"""

from functools import reduce

def filter_data(data, predicate):
    """
    Filter data using a predicate function.

    Demonstrates functional filter operation with lambda expressions.

    Args:
        data: List of items to filter
        predicate: Lambda function that returns True for items to keep

    Returns:
        List of filtered items
    """
    return list(filter(predicate, data))

def map_data(data, mapper):
    """
    Transform data using a mapper function.

    Demonstrates functional map operation with lambda expressions.

    Args:
        data: List of items to transform
        mapper: Lambda function to transform each item

    Returns:
        List of transformed items
    """
    return list(map(mapper, data))

def aggregate_data(data, reducer, initial):
    """
    Aggregate data using reduce operation.

    Demonstrates functional reduce pattern with lambda expressions.

    Args:
        data: List of items to aggregate
        reducer: Lambda function for reduction (accumulator, value) => result
        initial: Initial accumulator value

    Returns:
        Final aggregated result
    """
    return reduce(reducer, data, initial)

def group_and_sum(data, key_func):
    """
    Group data and sum revenue by key.

    Demonstrates grouping with lambda key extraction and aggregation.

    Args:
        data: List of dictionaries to group
        key_func: Lambda function to extract grouping key from each item

    Returns:
        Dictionary with keys and summed revenue values
    """
    groups = {}

    # Group items using key function
    for item in data:
        key = key_func(item)
        if key not in groups:
            groups[key] = 0

        # Sum revenue for each group
        groups[key] += item.get('revenue', 0)

    return groups

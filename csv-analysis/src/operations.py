from functools import reduce

def filter_data(data, predicate):
    return list(filter(predicate, data))

def map_data(data, mapper):
    return list(map(mapper, data))

def aggregate_data(data, reducer, initial):
    return reduce(reducer, data, initial)

def group_and_sum(data, key_func):
    groups = {}
    for item in data:
        key = key_func(item)
        if key not in groups:
            groups[key] = 0
        groups[key] += item.get('revenue', 0)
    return groups

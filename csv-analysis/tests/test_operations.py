import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.operations import filter_data, map_data, aggregate_data, group_and_sum


class TestOperations(unittest.TestCase):

    def setUp(self):
        self.sample_data = [
            {'id': 1, 'value': 10, 'category': 'A', 'revenue': 100},
            {'id': 2, 'value': 20, 'category': 'B', 'revenue': 200},
            {'id': 3, 'value': 30, 'category': 'A', 'revenue': 300},
            {'id': 4, 'value': 40, 'category': 'C', 'revenue': 400},
            {'id': 5, 'value': 50, 'category': 'B', 'revenue': 500},
        ]

    def test_filter_data_with_lambda(self):
        result = filter_data(self.sample_data, lambda x: x['value'] > 25)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(item['value'] > 25 for item in result))

    def test_filter_data_empty_result(self):
        result = filter_data(self.sample_data, lambda x: x['value'] > 100)
        self.assertEqual(len(result), 0)

    def test_filter_data_all_match(self):
        result = filter_data(self.sample_data, lambda x: x['value'] > 0)
        self.assertEqual(len(result), 5)

    def test_map_data_with_lambda(self):
        result = map_data(self.sample_data, lambda x: x['value'] * 2)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], 20)
        self.assertEqual(result[4], 100)

    def test_map_data_extract_field(self):
        result = map_data(self.sample_data, lambda x: x['category'])
        self.assertEqual(len(result), 5)
        self.assertEqual(result, ['A', 'B', 'A', 'C', 'B'])

    def test_map_data_transform(self):
        result = map_data(self.sample_data, lambda x: {'id': x['id'], 'doubled': x['value'] * 2})
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]['doubled'], 20)

    def test_aggregate_data_sum(self):
        values = [1, 2, 3, 4, 5]
        result = aggregate_data(values, lambda acc, x: acc + x, 0)
        self.assertEqual(result, 15)

    def test_aggregate_data_product(self):
        values = [2, 3, 4]
        result = aggregate_data(values, lambda acc, x: acc * x, 1)
        self.assertEqual(result, 24)

    def test_aggregate_data_max(self):
        values = [5, 2, 9, 1, 7]
        result = aggregate_data(values, lambda acc, x: max(acc, x), float('-inf'))
        self.assertEqual(result, 9)

    def test_aggregate_data_concatenate(self):
        values = ['a', 'b', 'c']
        result = aggregate_data(values, lambda acc, x: acc + x, '')
        self.assertEqual(result, 'abc')

    def test_aggregate_data_empty_list(self):
        result = aggregate_data([], lambda acc, x: acc + x, 10)
        self.assertEqual(result, 10)

    def test_group_and_sum(self):
        result = group_and_sum(self.sample_data, lambda x: x['category'])
        self.assertEqual(result['A'], 400)
        self.assertEqual(result['B'], 700)
        self.assertEqual(result['C'], 400)

    def test_group_and_sum_different_key(self):
        data = [
            {'name': 'Alice', 'revenue': 100},
            {'name': 'Bob', 'revenue': 200},
            {'name': 'Alice', 'revenue': 150},
        ]
        result = group_and_sum(data, lambda x: x['name'])
        self.assertEqual(result['Alice'], 250)
        self.assertEqual(result['Bob'], 200)

    def test_group_and_sum_single_group(self):
        data = [
            {'type': 'X', 'revenue': 100},
            {'type': 'X', 'revenue': 200},
            {'type': 'X', 'revenue': 300},
        ]
        result = group_and_sum(data, lambda x: x['type'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result['X'], 600)

    def test_group_and_sum_empty_data(self):
        result = group_and_sum([], lambda x: x['category'])
        self.assertEqual(len(result), 0)

    def test_group_and_sum_missing_revenue(self):
        data = [{'category': 'A'}, {'category': 'B', 'revenue': 100}]
        result = group_and_sum(data, lambda x: x['category'])
        self.assertEqual(result['A'], 0)
        self.assertEqual(result['B'], 100)

    def test_functional_composition(self):
        filtered = filter_data(self.sample_data, lambda x: x['value'] > 20)
        mapped = map_data(filtered, lambda x: x['revenue'])
        result = aggregate_data(mapped, lambda acc, x: acc + x, 0)
        self.assertEqual(result, 1200)


if __name__ == '__main__':
    unittest.main()

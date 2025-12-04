import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analyzer import SalesAnalyzer

class TestSalesAnalyzer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_csv = os.path.join(os.path.dirname(__file__), 'test_data.csv')

    def setUp(self):
        self.analyzer = SalesAnalyzer(self.test_csv)

    def test_initialization(self):
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(len(self.analyzer.data), 10)
        self.assertIn('revenue', self.analyzer.data.columns)
        self.assertIn('month', self.analyzer.data.columns)

    def test_revenue_calculation(self):
        first_row = self.analyzer.data.iloc[0]
        expected_revenue = first_row['quantity'] * first_row['price']
        self.assertEqual(first_row['revenue'], expected_revenue)

    def test_filter_by_with_lambda(self):
        filtered = self.analyzer.filter_by(lambda row: row['quantity'] > 2)
        self.assertTrue(all(filtered['quantity'] > 2))
        self.assertEqual(len(filtered), 5)

    def test_filter_by_empty_result(self):
        filtered = self.analyzer.filter_by(lambda row: row['quantity'] > 100)
        self.assertEqual(len(filtered), 0)

    def test_map_field_with_lambda(self):
        doubled_prices = self.analyzer.map_field(lambda row: row['price'] * 2)
        self.assertEqual(len(doubled_prices), 10)
        self.assertEqual(doubled_prices.iloc[0], 2000.00)

    def test_reduce_by_field(self):
        total_revenue = self.analyzer.reduce_by_field('revenue', lambda acc, x: acc + x)
        expected = self.analyzer.data['revenue'].sum()
        self.assertEqual(total_revenue, expected)

    def test_group_and_aggregate(self):
        result = self.analyzer.group_and_aggregate('category', 'revenue', lambda x: x.sum())
        self.assertIn('Electronics', result.index)
        self.assertIn('Furniture', result.index)
        self.assertIn('Clothing', result.index)

    def test_total_revenue_by_category(self):
        result = self.analyzer.total_revenue_by_category()
        self.assertEqual(len(result), 3)
        self.assertTrue(result.iloc[0] > result.iloc[1])

    def test_top_products(self):
        top3 = self.analyzer.top_products(3)
        self.assertEqual(len(top3), 3)
        self.assertEqual(top3.index[0], 'Laptop')

    def test_top_products_more_than_available(self):
        top20 = self.analyzer.top_products(20)
        self.assertLessEqual(len(top20), 10)

    def test_average_by_region(self):
        result = self.analyzer.average_by_region()
        self.assertEqual(len(result), 5)
        for region_avg in result:
            self.assertGreater(region_avg, 0)

    def test_monthly_trend(self):
        trend = self.analyzer.monthly_trend()
        self.assertGreater(len(trend), 0)
        self.assertTrue(trend.index.is_monotonic_increasing)

    def test_filter_high_quantity(self):
        high_qty = self.analyzer.filter_high_quantity(3)
        self.assertTrue(all(high_qty['quantity'] > 3))

    def test_filter_high_quantity_no_results(self):
        high_qty = self.analyzer.filter_high_quantity(100)
        self.assertEqual(len(high_qty), 0)

    def test_filter_by_category(self):
        electronics = self.analyzer.filter_by_category('Electronics')
        self.assertTrue(all(electronics['category'] == 'Electronics'))
        self.assertEqual(len(electronics), 5)

    def test_filter_by_category_case_sensitive(self):
        result = self.analyzer.filter_by_category('electronics')
        self.assertEqual(len(result), 0)

    def test_filter_date_range(self):
        q1 = self.analyzer.filter_date_range('2024-01-01', '2024-03-31')
        self.assertEqual(len(q1), 6)

    def test_filter_date_range_empty(self):
        future = self.analyzer.filter_date_range('2025-01-01', '2025-12-31')
        self.assertEqual(len(future), 0)

    def test_top_n_by_metric_with_lambda(self):
        top2 = self.analyzer.top_n_by_metric(2, lambda row: row['revenue'])
        self.assertEqual(len(top2), 2)

    def test_top_n_by_custom_metric(self):
        top3 = self.analyzer.top_n_by_metric(3, lambda row: row['quantity'] * row['price'])
        self.assertEqual(len(top3), 3)

    def test_aggregate_with_reduce(self):
        result = self.analyzer.aggregate_with_reduce('category')
        self.assertIn('Electronics', result)
        self.assertIn('Furniture', result)
        self.assertIn('Clothing', result)
        self.assertGreater(result['Electronics'], 0)

    def test_aggregate_with_reduce_by_region(self):
        result = self.analyzer.aggregate_with_reduce('region')
        self.assertEqual(len(result), 5)

    def test_summary_statistics(self):
        stats = self.analyzer.summary_statistics()
        self.assertEqual(stats['total_transactions'], 10)
        self.assertGreater(stats['total_revenue'], 0)
        self.assertGreater(stats['average_revenue'], 0)
        self.assertEqual(stats['categories'], 3)
        self.assertEqual(stats['regions'], 5)

    def test_summary_statistics_keys(self):
        stats = self.analyzer.summary_statistics()
        expected_keys = ['total_transactions', 'total_revenue', 'average_revenue', 'categories', 'regions']
        for key in expected_keys:
            self.assertIn(key, stats)

    def test_filter_chain_with_lambdas(self):
        result = self.analyzer.filter_by(lambda row: row['category'] == 'Electronics')
        result = result[result.apply(lambda row: row['quantity'] > 1, axis=1)]
        self.assertTrue(all(result['category'] == 'Electronics'))
        self.assertTrue(all(result['quantity'] > 1))

    def test_data_immutability_after_filter(self):
        original_length = len(self.analyzer.data)
        self.analyzer.filter_by(lambda row: row['quantity'] > 5)
        self.assertEqual(len(self.analyzer.data), original_length)

if __name__ == '__main__':
    unittest.main()

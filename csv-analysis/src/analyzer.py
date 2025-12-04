import pandas as pd
from functools import reduce

class SalesAnalyzer:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.data['revenue'] = self.data['quantity'] * self.data['price']
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data['month'] = self.data['date'].dt.to_period('M')

    def filter_by(self, predicate):
        return self.data[self.data.apply(predicate, axis=1)].copy()

    def map_field(self, mapper):
        return self.data.apply(mapper, axis=1)

    def reduce_by_field(self, field, reducer, initial=0):
        return reduce(reducer, self.data[field], initial)

    def group_and_aggregate(self, group_by, agg_field, agg_func):
        return self.data.groupby(group_by)[agg_field].apply(agg_func).sort_values(ascending=False)

    def total_revenue_by_category(self):
        return self.group_and_aggregate('category', 'revenue', lambda x: x.sum())

    def top_products(self, n=5):
        return self.group_and_aggregate('product', 'revenue', lambda x: x.sum()).head(n)

    def average_by_region(self):
        return self.group_and_aggregate('region', 'revenue', lambda x: x.mean())

    def monthly_trend(self):
        return self.data.groupby('month')['revenue'].apply(lambda x: x.sum()).sort_index()

    def filter_high_quantity(self, threshold):
        return self.filter_by(lambda row: row['quantity'] > threshold)

    def filter_by_category(self, category):
        return self.filter_by(lambda row: row['category'] == category)

    def filter_date_range(self, start_date, end_date):
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return self.filter_by(lambda row: start <= row['date'] <= end)

    def top_n_by_metric(self, n, metric_func):
        metrics = self.map_field(metric_func)
        indices = metrics.nlargest(n).index
        return self.data.loc[indices]

    def aggregate_with_reduce(self, group_field):
        groups = {}
        for _, row in self.data.iterrows():
            key = row[group_field]
            if key not in groups:
                groups[key] = []
            groups[key].append(row['revenue'])

        return {
            key: reduce(lambda acc, val: acc + val, values, 0)
            for key, values in groups.items()
        }

    def summary_statistics(self):
        return {
            'total_transactions': len(self.data),
            'total_revenue': self.reduce_by_field('revenue', lambda acc, x: acc + x),
            'average_revenue': self.data['revenue'].mean(),
            'categories': self.data['category'].nunique(),
            'regions': self.data['region'].nunique()
        }

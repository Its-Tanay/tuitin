import pandas as pd
from functools import reduce
from datetime import datetime

class SalesAnalyzer:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.data['revenue'] = self.data['quantity'] * self.data['price']
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data['month'] = self.data['date'].dt.to_period('M')

    def filter_by(self, predicate):
        filtered = self.data[self.data.apply(predicate, axis=1)].copy()
        return filtered

    def map_transform(self, transformer):
        return self.data.apply(transformer, axis=1)

    def group_and_aggregate(self, group_by, aggregations):
        return self.data.groupby(group_by).agg(aggregations)

    def total_revenue_by_category(self):
        return (self.data.groupby('category')['revenue']
                .sum()
                .sort_values(ascending=False))

    def top_products_by_sales(self, n=5):
        return (self.data.groupby('product')['revenue']
                .sum()
                .sort_values(ascending=False)
                .head(n))

    def average_order_value_by_region(self):
        return (self.data.groupby('region')['revenue']
                .mean()
                .sort_values(ascending=False))

    def monthly_sales_trend(self):
        return (self.data.groupby('month')['revenue']
                .sum()
                .sort_index())

    def filter_high_quantity_sales(self, threshold):
        return self.filter_by(lambda row: row['quantity'] > threshold)

    def revenue_by_region_and_category(self):
        return (self.data.groupby(['region', 'category'])['revenue']
                .sum()
                .sort_values(ascending=False))

    def highest_revenue_transaction(self):
        return self.data.loc[self.data['revenue'].idxmax()]

    def filter_by_date_range(self, start_date, end_date):
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return self.filter_by(lambda row: start <= row['date'] <= end)

    def custom_aggregation_with_reduce(self, group_field, value_field):
        groups = {}
        for _, row in self.data.iterrows():
            key = row[group_field]
            if key not in groups:
                groups[key] = []
            groups[key].append(row[value_field])

        return {
            key: reduce(lambda acc, val: acc + val, values, 0)
            for key, values in groups.items()
        }

    def apply_discount_lambda(self, discount_rate):
        return self.data.apply(
            lambda row: {**row.to_dict(), 'discounted_price': row['price'] * (1 - discount_rate)},
            axis=1
        )

    def filter_and_transform(self, filter_lambda, transform_lambda):
        filtered = self.data[self.data.apply(filter_lambda, axis=1)]
        return filtered.apply(transform_lambda, axis=1)

    def top_n_by_custom_metric(self, n, metric_lambda):
        self.data['custom_metric'] = self.data.apply(metric_lambda, axis=1)
        result = self.data.nlargest(n, 'custom_metric')[['transaction_id', 'product', 'custom_metric']]
        self.data.drop('custom_metric', axis=1, inplace=True)
        return result

    def category_statistics_with_lambdas(self):
        return self.data.groupby('category').agg({
            'revenue': [
                ('total', lambda x: x.sum()),
                ('average', lambda x: x.mean()),
                ('max', lambda x: x.max()),
                ('count', lambda x: x.count())
            ]
        })

    def region_performance_score(self):
        return self.data.groupby('region').apply(
            lambda group: (group['revenue'].sum() / group['revenue'].count()) * group['quantity'].sum()
        ).sort_values(ascending=False)

def main():
    analyzer = SalesAnalyzer('sales_data.csv')

    print("--- Sales Data Analysis ---\n")

    print("1. Total Revenue by Category:")
    print(analyzer.total_revenue_by_category())
    print()

    print("2. Top 5 Products by Sales:")
    print(analyzer.top_products_by_sales())
    print()

    print("3. Average Order Value by Region:")
    print(analyzer.average_order_value_by_region())
    print()

    print("4. Monthly Sales Trend:")
    print(analyzer.monthly_sales_trend())
    print()

    print("5. High Quantity Sales (>5 items):")
    high_qty = analyzer.filter_high_quantity_sales(5)
    print(f"Found {len(high_qty)} transactions")
    print()

    print("6. Revenue by Region and Category (Top 10):")
    print(analyzer.revenue_by_region_and_category().head(10))
    print()

    print("7. Highest Revenue Transaction:")
    print(analyzer.highest_revenue_transaction())
    print()

    print("8. Sales in Q1 2024:")
    q1_sales = analyzer.filter_by_date_range('2024-01-01', '2024-03-31')
    print(f"Total Q1 Revenue: ${q1_sales['revenue'].sum():.2f}")
    print()

    print("9. Custom Aggregation with Reduce (Revenue by Category):")
    reduce_result = analyzer.custom_aggregation_with_reduce('category', 'revenue')
    for category, total in sorted(reduce_result.items(), key=lambda x: x[1], reverse=True):
        print(f"{category}: ${total:.2f}")
    print()

    print("10. Category Statistics with Lambda Aggregations:")
    print(analyzer.category_statistics_with_lambdas())
    print()

    print("11. Top 5 Transactions by Custom Metric (revenue * quantity):")
    top_custom = analyzer.top_n_by_custom_metric(5, lambda row: row['revenue'] * row['quantity'])
    print(top_custom)
    print()

    print("12. Region Performance Score:")
    print(analyzer.region_performance_score())
    print()

if __name__ == '__main__':
    main()
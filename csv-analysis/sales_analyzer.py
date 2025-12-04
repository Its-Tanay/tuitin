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

if __name__ == '__main__':
    main()
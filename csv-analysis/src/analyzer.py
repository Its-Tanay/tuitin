import pandas as pd
from functools import reduce

class SalesAnalyzer:
    """
    Sales data analyzer using functional programming patterns.

    This class demonstrates proficiency with stream operations, lambda expressions,
    and functional programming paradigms for CSV data analysis.
    """

    def __init__(self, csv_path):
        """
        Initialize the analyzer with sales data from CSV file.

        Automatically calculates revenue and parses dates for time-series analysis.

        Args:
            csv_path: Path to the CSV file containing sales data
        """
        self.data = pd.read_csv(csv_path)

        # Calculate revenue for each transaction
        self.data['revenue'] = self.data['quantity'] * self.data['price']

        # Parse dates for time-based filtering and analysis
        self.data['date'] = pd.to_datetime(self.data['date'])

        # Extract month for time-series aggregation
        self.data['month'] = self.data['date'].dt.to_period('M')

    def filter_by(self, predicate):
        """
        Filter data using a lambda predicate function.

        Demonstrates functional programming with lambda expressions for filtering.

        Args:
            predicate: Lambda function that takes a row and returns boolean

        Returns:
            Filtered DataFrame copy
        """
        return self.data[self.data.apply(predicate, axis=1)].copy()

    def map_field(self, mapper):
        """
        Transform data using a mapper function.

        Demonstrates map operation with lambda expressions.

        Args:
            mapper: Lambda function to transform each row

        Returns:
            Series of transformed values
        """
        return self.data.apply(mapper, axis=1)

    def reduce_by_field(self, field, reducer, initial=0):
        """
        Aggregate field values using reduce operation.

        Demonstrates functional reduce pattern with lambda expressions.

        Args:
            field: Column name to reduce
            reducer: Lambda function for reduction (acc, value) => result
            initial: Initial accumulator value

        Returns:
            Final reduced value
        """
        return reduce(reducer, self.data[field], initial)

    def group_and_aggregate(self, group_by, agg_field, agg_func):
        """
        Group data and apply aggregation function.

        Demonstrates grouping operations with lambda aggregations.

        Args:
            group_by: Field to group by
            agg_field: Field to aggregate
            agg_func: Lambda aggregation function

        Returns:
            Series with grouped and aggregated results, sorted descending
        """
        return self.data.groupby(group_by)[agg_field].apply(agg_func).sort_values(ascending=False)

    def total_revenue_by_category(self):
        """
        Calculate total revenue for each category using lambda aggregation.

        Returns:
            Series with revenue totals per category, sorted by revenue
        """
        return self.group_and_aggregate('category', 'revenue', lambda x: x.sum())

    def top_products(self, n=5):
        """
        Find top N products by revenue using lambda aggregation.

        Args:
            n: Number of top products to return

        Returns:
            Series with top N products and their revenues
        """
        return self.group_and_aggregate('product', 'revenue', lambda x: x.sum()).head(n)

    def average_by_region(self):
        """
        Calculate average revenue per region using lambda aggregation.

        Returns:
            Series with average revenue per region
        """
        return self.group_and_aggregate('region', 'revenue', lambda x: x.mean())

    def monthly_trend(self):
        """
        Analyze monthly sales trend using time-series grouping.

        Demonstrates time-based aggregation with lambda expressions.

        Returns:
            Series with monthly revenue totals, chronologically sorted
        """
        return self.data.groupby('month')['revenue'].apply(lambda x: x.sum()).sort_index()

    def filter_high_quantity(self, threshold):
        """
        Filter transactions with quantity above threshold using lambda.

        Args:
            threshold: Minimum quantity value

        Returns:
            Filtered DataFrame with high-quantity transactions
        """
        return self.filter_by(lambda row: row['quantity'] > threshold)

    def filter_by_category(self, category):
        """
        Filter transactions by category using lambda predicate.

        Args:
            category: Category name to filter by

        Returns:
            Filtered DataFrame with matching category
        """
        return self.filter_by(lambda row: row['category'] == category)

    def filter_date_range(self, start_date, end_date):
        """
        Filter transactions within date range using lambda predicate.

        Args:
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)

        Returns:
            Filtered DataFrame with transactions in date range
        """
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return self.filter_by(lambda row: start <= row['date'] <= end)

    def top_n_by_metric(self, n, metric_func):
        """
        Find top N items by custom metric using lambda function.

        Demonstrates map operation combined with selection.

        Args:
            n: Number of top items to return
            metric_func: Lambda function to calculate metric for each row

        Returns:
            DataFrame with top N items by custom metric
        """
        # Map custom metric across all rows
        metrics = self.map_field(metric_func)

        # Get indices of top N values
        indices = metrics.nlargest(n).index

        return self.data.loc[indices]

    def aggregate_with_reduce(self, group_field):
        """
        Group and sum using functional reduce pattern.

        Demonstrates manual grouping with reduce and lambda expressions.

        Args:
            group_field: Field to group by

        Returns:
            Dictionary with group keys and revenue totals
        """
        # Manual grouping using iteration
        groups = {}
        for _, row in self.data.iterrows():
            key = row[group_field]
            if key not in groups:
                groups[key] = []
            groups[key].append(row['revenue'])

        # Apply reduce with lambda to each group
        return {
            key: reduce(lambda acc, val: acc + val, values, 0)
            for key, values in groups.items()
        }

    def summary_statistics(self):
        """
        Generate summary statistics using various functional operations.

        Combines multiple functional programming patterns.

        Returns:
            Dictionary with key summary statistics
        """
        return {
            'total_transactions': len(self.data),
            'total_revenue': self.reduce_by_field('revenue', lambda acc, x: acc + x),
            'average_revenue': self.data['revenue'].mean(),
            'categories': self.data['category'].nunique(),
            'regions': self.data['region'].nunique()
        }

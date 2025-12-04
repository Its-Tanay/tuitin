import sys
sys.path.insert(0, '..')

from main import SalesAnalyzer

def main():
    analyzer = SalesAnalyzer('../data/sales_data.csv')

    print("--- Sales Data Analysis with Functional Programming ---\n")

    print("1. Total Revenue by Category (using lambda aggregation):")
    print(analyzer.total_revenue_by_category())
    print()

    print("2. Top 5 Products by Sales:")
    print(analyzer.top_products(5))
    print()

    print("3. Average Revenue by Region:")
    print(analyzer.average_by_region())
    print()

    print("4. Monthly Sales Trend (time-series):")
    print(analyzer.monthly_trend())
    print()

    print("5. High Quantity Transactions (filter with lambda, quantity > 5):")
    high_qty = analyzer.filter_high_quantity(5)
    print(f"Found {len(high_qty)} transactions with quantity > 5")
    print(high_qty.head()[['transaction_id', 'product', 'quantity', 'revenue']])
    print()

    print("6. Electronics Sales (filter by category):")
    electronics = analyzer.filter_by_category('Electronics')
    print(f"Total Electronics Revenue: ${electronics['revenue'].sum():.2f}")
    print()

    print("7. Q1 2024 Sales (filter by date range):")
    q1_sales = analyzer.filter_date_range('2024-01-01', '2024-03-31')
    print(f"Q1 Transactions: {len(q1_sales)}")
    print(f"Q1 Revenue: ${q1_sales['revenue'].sum():.2f}")
    print()

    print("8. Top 3 by Custom Metric (using map and lambda):")
    top_custom = analyzer.top_n_by_metric(3, lambda row: row['revenue'] * row['quantity'])
    print(top_custom[['transaction_id', 'product', 'revenue', 'quantity']])
    print()

    print("9. Category Totals with Reduce:")
    reduce_result = analyzer.aggregate_with_reduce('category')
    for category, total in sorted(reduce_result.items(), key=lambda x: x[1], reverse=True):
        print(f"{category}: ${total:.2f}")
    print()

    print("10. Summary Statistics:")
    stats = analyzer.summary_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: ${value:.2f}" if 'revenue' in key else f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    print()

if __name__ == '__main__':
    main()

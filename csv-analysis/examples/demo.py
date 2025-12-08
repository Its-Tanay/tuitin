import sys
sys.path.insert(0, '..')

from main import SalesAnalyzer


def execute_query(analyzer, query):
    """Parse and execute user query"""
    query = query.lower().strip()

    # Revenue by category
    if 'revenue by category' in query or 'category revenue' in query:
        print("\nRevenue by Category:")
        print("  (Sum of all revenue grouped by product category)")
        print()
        revenue = analyzer.total_revenue_by_category()
        for category, value in revenue.items():
            print(f"  {category}: ${value:,.2f}")
        print(f"\n  Total: ${revenue.sum():,.2f}")
        return True

    # Top products
    elif query.startswith('top') and 'product' in query:
        import re
        match = re.search(r'\d+', query)
        n = int(match.group()) if match else 5

        print(f"\nTop {n} Products by Revenue:")
        print(f"  (Products ranked by total sales revenue)")
        print()
        top = analyzer.top_products(n)
        for idx, (product, revenue) in enumerate(top.items(), 1):
            print(f"  {idx}. {product}: ${revenue:,.2f}")
        return True

    # Average by region
    elif 'average' in query and 'region' in query:
        print("\nAverage Revenue by Region:")
        print("  (Mean revenue per transaction for each region)")
        print()
        avg = analyzer.average_by_region()
        for region, value in sorted(avg.items(), key=lambda x: x[1], reverse=True):
            print(f"  {region}: ${value:,.2f}")
        return True

    # Monthly trend
    elif 'monthly' in query or 'trend' in query:
        print("\nMonthly Revenue Trend:")
        print("  (Total revenue aggregated by month)")
        print()
        trend = analyzer.monthly_trend()
        for month, value in trend.items():
            print(f"  {month}: ${value:,.2f}")
        return True

    # Filter by category
    elif 'filter' in query and 'category' in query:
        categories = ['electronics', 'clothing', 'home']
        category = None
        for cat in categories:
            if cat in query:
                category = cat.capitalize()
                break

        if category:
            print(f"\n{category} Category Analysis:")
            print(f"  (Filtered dataset for category = '{category}')")
            print()
            filtered = analyzer.filter_by_category(category)
            revenue_sum = filtered['revenue'].sum()
            count = len(filtered)
            avg = filtered['revenue'].mean()

            print(f"  Count: {count} transactions")
            print(f"  Total Revenue: ${revenue_sum:,.2f}")
            print(f"  Average Revenue: ${avg:,.2f}")

            print(f"\n  Top 3 products in {category}:")
            top_items = filtered.nlargest(3, 'revenue')[['product', 'revenue']]
            for idx, row in top_items.iterrows():
                print(f"    {row['product']}: ${row['revenue']:,.2f}")
            return True
        else:
            print("\n[ERROR] Category not found. Available: electronics, clothing, home")
            return False

    # High quantity
    elif 'high quantity' in query or 'quantity >' in query:
        import re
        match = re.search(r'\d+', query)
        threshold = int(match.group()) if match else 5

        print(f"\nHigh Quantity Filter (quantity > {threshold}):")
        print(f"  (Transactions where quantity exceeds {threshold})")
        print()
        high_qty = analyzer.filter_high_quantity(threshold)
        print(f"  Found {len(high_qty)} matching transactions")
        print(f"  Total Revenue: ${high_qty['revenue'].sum():,.2f}")
        print(f"  Average Quantity: {high_qty['quantity'].mean():.1f}")
        return True

    # Date range queries
    elif 'q1' in query or 'q2' in query or 'q3' in query or 'q4' in query:
        if 'q1' in query:
            start, end = '2024-01-01', '2024-03-31'
            period = "Q1 2024"
        elif 'q2' in query:
            start, end = '2024-04-01', '2024-06-30'
            period = "Q2 2024"
        elif 'q3' in query:
            start, end = '2024-07-01', '2024-09-30'
            period = "Q3 2024"
        else:
            start, end = '2024-10-01', '2024-12-31'
            period = "Q4 2024"

        print(f"\n{period} Sales Analysis:")
        print(f"  (Date range: {start} to {end})")
        print()
        filtered = analyzer.filter_date_range(start, end)
        revenue_sum = filtered['revenue'].sum()
        count = len(filtered)

        print(f"  Transactions: {count}")
        print(f"  Total Revenue: ${revenue_sum:,.2f}")
        print(f"  Average Revenue: ${revenue_sum / count if count > 0 else 0:,.2f}")
        return True

    # Summary statistics
    elif 'summary' in query or 'statistics' in query or 'stats' in query:
        print("\nSummary Statistics:")
        print("  (Descriptive statistics for the entire dataset)")
        print()
        stats = analyzer.summary_statistics()

        print(f"  Total Transactions: {stats['total_transactions']}")
        print(f"  Total Revenue: ${stats['total_revenue']:,.2f}")
        print(f"  Average Revenue: ${stats['average_revenue']:,.2f}")
        print(f"  Median Revenue: ${stats['median_revenue']:,.2f}")
        print(f"  Standard Deviation: ${stats['std_revenue']:,.2f}")
        print(f"  Min Revenue: ${stats['min_revenue']:,.2f}")
        print(f"  Max Revenue: ${stats['max_revenue']:,.2f}")
        return True

    # Custom metric
    elif 'custom metric' in query:
        print("\nCustom Metric Analysis (Revenue * Quantity):")
        print("  (Products ranked by revenue multiplied by quantity sold)")
        print()
        top = analyzer.top_n_by_metric(5, lambda row: row['revenue'] * row['quantity'])

        for idx, row in top.iterrows():
            metric_value = row['revenue'] * row['quantity']
            print(f"  {row['product']}: ${row['revenue']:,.2f} * {row['quantity']} = ${metric_value:,.2f}")
        return True

    # Count by category
    elif 'count' in query and 'category' in query:
        print("\nTransaction Count by Category:")
        print("  (Number of transactions in each category)")
        print()
        counts = analyzer.data.groupby('category').size()
        for category, count in counts.items():
            print(f"  {category}: {count} transactions")
        print(f"\n  Total: {counts.sum()} transactions")
        return True

    # Help
    elif query in ['help', 'h', '?']:
        show_help()
        return True

    # Exit
    elif query in ['exit', 'quit', 'q']:
        return 'exit'

    else:
        print("\n[ERROR] Query not recognized. Type 'help' for available queries.")
        return False


def show_welcome():
    """Display welcome screen"""
    print("\n" + "=" * 60)
    print("  Sales Data Analysis Tool")
    print("=" * 60)
    print("\nDemonstrates functional programming patterns:")
    print("  - filter() for data subsetting")
    print("  - map() for transformations")
    print("  - reduce() for aggregations")
    print("  - lambda expressions for custom operations")
    print()


def show_help():
    """Display help with example queries"""
    print("\n" + "-" * 60)
    print("Available Queries")
    print("-" * 60)

    print("\nAggregations:")
    print("  revenue by category    - Sum revenue grouped by category")
    print("  top 5 products         - Top N products by revenue")
    print("  average by region      - Mean revenue per region")
    print("  monthly trend          - Revenue totals by month")
    print("  count by category      - Transaction counts by category")

    print("\nFiltering:")
    print("  filter category electronics  - Subset by category")
    print("  high quantity 5              - Transactions with qty > N")
    print("  q1                           - Q1 2024 data")
    print("  q2                           - Q2 2024 data")

    print("\nStatistics:")
    print("  summary                - Descriptive statistics")
    print("  custom metric          - Revenue * Quantity ranking")

    print("\nCommands:")
    print("  help                   - Show this help")
    print("  exit                   - Quit program")
    print()


def show_dataset_info(analyzer):
    """Show information about loaded dataset"""
    print("-" * 60)
    print("Dataset Loaded")
    print("-" * 60)

    total_records = len(analyzer.data)
    total_revenue = analyzer.data['revenue'].sum()
    date_range = f"{analyzer.data['date'].min()} to {analyzer.data['date'].max()}"
    categories = ', '.join(sorted(analyzer.data['category'].unique()))

    print(f"  Records: {total_records:,}")
    print(f"  Total Revenue: ${total_revenue:,.2f}")
    print(f"  Date Range: {date_range}")
    print(f"  Categories: {categories}")
    print()


def main():
    """Main interactive loop"""
    show_welcome()

    # Load data
    print("Loading sales_data.csv...")
    try:
        analyzer = SalesAnalyzer('data/sales_data.csv')
        print("[OK] Data loaded successfully\n")
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return

    # Show dataset info
    show_dataset_info(analyzer)

    print("Type 'help' for available queries\n")
    print("=" * 60)

    # Interactive query loop
    while True:
        try:
            query = input("\n> ").strip()

            if not query:
                continue

            result = execute_query(analyzer, query)

            if result == 'exit':
                print("\nGoodbye.\n")
                break

        except KeyboardInterrupt:
            print("\n\nInterrupted.\n")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            print("Try 'help' for available queries\n")


if __name__ == '__main__':
    main()

# CSV Sales Data Analysis

A functional programming utility for analyzing sales data from CSV files. Demonstrates proficiency with stream operations, lambda expressions, and data aggregation patterns.

## Features

- **Functional Programming Paradigms**: Filter, map, reduce operations with lambda expressions
- **Sales Analytics**: Revenue analysis by category, product, region, and time period
- **Time-Series Analysis**: Monthly trends and date range filtering
- **Data Aggregation**: Group-by operations with custom aggregation functions
- **Flexible API**: Plug-and-play utility for easy integration

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install pandas
```

## Usage

The main entry point is `main.py` which exports the core functionality:

```python
from main import SalesAnalyzer, filter_data, map_data, aggregate_data, group_and_sum

# Initialize analyzer with CSV file
analyzer = SalesAnalyzer('data/sales_data.csv')

# Filter data with lambda predicate
high_value = analyzer.filter_by(lambda row: row['revenue'] > 1000)

# Get top products by revenue
top_products = analyzer.top_products(5)

# Analyze monthly trends
monthly_revenue = analyzer.monthly_trend()

# Custom aggregation with lambda
total = analyzer.reduce_by_field('revenue', lambda acc, x: acc + x)
```

See `examples/demo.py` for comprehensive usage examples.

## Sample Output

```
=== Sales Analysis Demo ===

Summary Statistics:
Total Transactions: 500
Total Revenue: $315,775.00
Average Revenue: $631.55
Categories: 5
Regions: 5

Top 5 Products by Revenue:
Laptop         $45,000.00
Monitor        $22,500.00
Desk           $18,500.00
Chair          $15,000.00
Smartphone     $12,000.00

Revenue by Category:
Electronics    $125,000.00
Furniture       $85,000.00
Clothing        $55,000.00
Home            $30,000.00
Sports          $20,775.00

Monthly Revenue Trend:
2024-01        $52,150.00
2024-02        $48,325.00
2024-03        $55,100.00
2024-04        $49,800.00
2024-05        $58,200.00
2024-06        $52,200.00
```

## Running Tests

Execute the test suite:

```bash
python -m unittest discover tests
```

Run specific test modules:

```bash
python -m unittest tests.test_analyzer
python -m unittest tests.test_operations
```

All tests should pass (43 tests total).

## Project Structure

```
csv-analysis/
├── main.py              # API entry point
├── src/
│   ├── analyzer.py      # SalesAnalyzer class
│   └── operations.py    # Functional operations
├── data/
│   └── sales_data.csv   # Sales dataset (500 records)
├── tests/
│   ├── test_analyzer.py
│   ├── test_operations.py
│   └── test_data.csv
├── examples/
│   └── demo.py          # Usage examples
└── generate_data.py     # Data generation script
```

## Functional Programming Features

- **Lambda Expressions**: Used extensively for predicates, mappers, and reducers
- **Filter Operations**: Data filtering with custom predicates
- **Map Operations**: Data transformation and field extraction
- **Reduce Operations**: Aggregation using functools.reduce
- **Stream Processing**: Chaining functional operations for complex analysis
- **Immutability**: Filter operations return copies, preserving original data

import csv
import random
from datetime import datetime, timedelta

products = [
    ('Laptop', 'Electronics', 1200),
    ('Mouse', 'Electronics', 25),
    ('Keyboard', 'Electronics', 75),
    ('Monitor', 'Electronics', 300),
    ('Headphones', 'Electronics', 150),
    ('Desk', 'Furniture', 450),
    ('Chair', 'Furniture', 200),
    ('Bookshelf', 'Furniture', 180),
    ('Lamp', 'Furniture', 60),
    ('Sofa', 'Furniture', 800),
    ('T-Shirt', 'Clothing', 25),
    ('Jeans', 'Clothing', 60),
    ('Jacket', 'Clothing', 120),
    ('Sneakers', 'Clothing', 80),
    ('Dress', 'Clothing', 90),
    ('Coffee Maker', 'Appliances', 80),
    ('Blender', 'Appliances', 60),
    ('Toaster', 'Appliances', 40),
    ('Microwave', 'Appliances', 150),
    ('Vacuum', 'Appliances', 200),
]

regions = ['North', 'South', 'East', 'West', 'Central']

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 30)

def generate_sales_data(num_records=500):
    data = []

    for i in range(1, num_records + 1):
        product_name, category, base_price = random.choice(products)
        region = random.choice(regions)

        days_offset = random.randint(0, (end_date - start_date).days)
        transaction_date = start_date + timedelta(days=days_offset)

        price_variation = random.uniform(0.9, 1.1)
        price = round(base_price * price_variation, 2)

        if category == 'Electronics':
            quantity = random.randint(1, 5)
        elif category == 'Furniture':
            quantity = random.randint(1, 3)
        else:
            quantity = random.randint(1, 10)

        data.append({
            'transaction_id': i,
            'date': transaction_date.strftime('%Y-%m-%d'),
            'product': product_name,
            'category': category,
            'region': region,
            'quantity': quantity,
            'price': price
        })

    return data

def write_to_csv(data, filename='sales_data.csv'):
    fieldnames = ['transaction_id', 'date', 'product', 'category', 'region', 'quantity', 'price']

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Generated {len(data)} records in {filename}")

if __name__ == '__main__':
    sales_data = generate_sales_data(500)
    write_to_csv(sales_data)

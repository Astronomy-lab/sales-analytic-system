# utils/data_processor.py

def calculate_total_revenue(transactions):
    total = 0.0
    for t in transactions:
        total += t['Quantity'] * t['UnitPrice']
    return total


def region_wise_sales(transactions):
    region_data = {}
    total_sales = calculate_total_revenue(transactions)

    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1

    for region in region_data:
        region_data[region]['percentage'] = round(
            (region_data[region]['total_sales'] / total_sales) * 100, 2
        )

    return dict(sorted(
        region_data.items(),
        key=lambda x: x[1]['total_sales'],
        reverse=True
    ))


def top_selling_products(transactions, n=5):
    products = {}

    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']

        if name not in products:
            products[name] = {'qty': 0, 'revenue': 0.0}

        products[name]['qty'] += qty
        products[name]['revenue'] += revenue

    sorted_products = sorted(
        products.items(),
        key=lambda x: x[1]['qty'],
        reverse=True
    )

    return [
        (name, data['qty'], data['revenue'])
        for name, data in sorted_products[:n]
    ]


def customer_analysis(transactions):
    customers = {}

    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']

        if cid not in customers:
            customers[cid] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products': set()
            }

        customers[cid]['total_spent'] += amount
        customers[cid]['purchase_count'] += 1
        customers[cid]['products'].add(t['ProductName'])

    for cid in customers:
        customers[cid]['avg_order_value'] = round(
            customers[cid]['total_spent'] / customers[cid]['purchase_count'], 2
        )
        customers[cid]['products_bought'] = list(customers[cid]['products'])
        del customers[cid]['products']

    return dict(sorted(
        customers.items(),
        key=lambda x: x[1]['total_spent'],
        reverse=True
    ))


def daily_sales_trend(transactions):
    daily = {}

    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']

        if date not in daily:
            daily[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }

        daily[date]['revenue'] += amount
        daily[date]['transaction_count'] += 1
        daily[date]['customers'].add(t['CustomerID'])

    for date in daily:
        daily[date]['unique_customers'] = len(daily[date]['customers'])
        del daily[date]['customers']

    return dict(sorted(daily.items()))


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = 0.0
    peak_count = 0

    for date, stats in daily.items():
        if stats['revenue'] > peak_revenue:
            peak_revenue = stats['revenue']
            peak_count = stats['transaction_count']
            peak_date = date

    return (peak_date, peak_revenue, peak_count)
#------------------------------------------------
#---------------------------------------------
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    """

    products = {}

    # Step 1: Aggregate quantity and revenue per product
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']

        if name not in products:
            products[name] = {
                'total_qty': 0,
                'total_revenue': 0.0
            }

        products[name]['total_qty'] += qty
        products[name]['total_revenue'] += revenue

    # Step 2: Filter low performing products
    low_products = []

    for name, data in products.items():
        if data['total_qty'] < threshold:
            low_products.append(
                (name, data['total_qty'], data['total_revenue'])
            )

    # Step 3: Sort by quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products



#-------------------------------------------------
def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    import os
    from datetime import datetime
    from collections import defaultdict

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # ---------------- BASIC STATS ----------------
    total_transactions = len(transactions)
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted(t['Date'] for t in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    # ---------------- REGION PERFORMANCE ----------------
    region_data = defaultdict(lambda: {'revenue': 0, 'count': 0})

    for t in transactions:
        amount = t['Quantity'] * t['UnitPrice']
        region_data[t['Region']]['revenue'] += amount
        region_data[t['Region']]['count'] += 1

    region_stats = []
    for region, data in region_data.items():
        percent = (data['revenue'] / total_revenue) * 100 if total_revenue else 0
        region_stats.append((region, data['revenue'], percent, data['count']))

    region_stats.sort(key=lambda x: x[1], reverse=True)

    # ---------------- PRODUCT DATA ----------------
    product_data = defaultdict(lambda: {'qty': 0, 'rev': 0})

    for t in transactions:
        product_data[t['ProductName']]['qty'] += t['Quantity']
        product_data[t['ProductName']]['rev'] += t['Quantity'] * t['UnitPrice']

    top_products = sorted(
        product_data.items(),
        key=lambda x: x[1]['qty'],
        reverse=True
    )[:5]

    low_products = [
        (p, d['qty'], d['rev'])
        for p, d in product_data.items()
        if d['qty'] < 10
    ]

    # ---------------- CUSTOMER DATA ----------------
    customer_data = defaultdict(lambda: {'spent': 0, 'count': 0})

    for t in transactions:
        customer_data[t['CustomerID']]['spent'] += t['Quantity'] * t['UnitPrice']
        customer_data[t['CustomerID']]['count'] += 1

    top_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1]['spent'],
        reverse=True
    )[:5]

    # ---------------- DAILY TREND ----------------
    daily_data = defaultdict(lambda: {'rev': 0, 'count': 0, 'customers': set()})

    for t in transactions:
        amount = t['Quantity'] * t['UnitPrice']
        daily_data[t['Date']]['rev'] += amount
        daily_data[t['Date']]['count'] += 1
        daily_data[t['Date']]['customers'].add(t['CustomerID'])

    daily_trend = sorted(daily_data.items())

    # ---------------- API ENRICHMENT ----------------
    enriched_success = [t for t in enriched_transactions if t.get('API_Match')]
    enriched_failed = [t for t in enriched_transactions if not t.get('API_Match')]

    success_rate = (
        (len(enriched_success) / len(enriched_transactions)) * 100
        if enriched_transactions else 0
    )

    failed_products = sorted(set(t['ProductName'] for t in enriched_failed))

    # ---------------- WRITE REPORT ----------------
    with open(output_file, 'w', encoding='utf-8') as f:

        f.write("=" * 44 + "\n")
        f.write("       SALES ANALYTICS REPORT\n")
        f.write(f"   Generated: {datetime.now()}\n")
        f.write(f"   Records Processed: {total_transactions}\n")
        f.write("=" * 44 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write("Region     Sales (₹)     % Total   Transactions\n")
        for r, rev, pct, cnt in region_stats:
            f.write(f"{r:<10} ₹{rev:>10,.0f}     {pct:>6.2f}%      {cnt}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        for i, (name, d) in enumerate(top_products, 1):
            f.write(f"{i}. {name} | Qty: {d['qty']} | Revenue: ₹{d['rev']:,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        for i, (cid, d) in enumerate(top_customers, 1):
            f.write(f"{i}. {cid} | Spent: ₹{d['spent']:,.2f} | Orders: {d['count']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        for date, d in daily_trend:
            f.write(
                f"{date} | Revenue: ₹{d['rev']:,.2f} | "
                f"Transactions: {d['count']} | "
                f"Customers: {len(d['customers'])}\n"
            )
        f.write("\n")

        f.write("LOW PERFORMING PRODUCTS\n")
        f.write("-" * 44 + "\n")
        for p, q, r in low_products:
            f.write(f"- {p} | Qty: {q} | Revenue: ₹{r:,.2f}\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Products Enriched: {len(enriched_success)}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Failed Products:\n")
        for p in failed_products:
            f.write(f"- {p}\n")

    print(" Sales report generated at:", output_file)
from collections import defaultdict


# -----------------------------------------
def calculate_total_revenue(data):
    return sum(t['Quantity'] * t['UnitPrice'] for t in data)


# -----------------------------------------
def region_wise_sales(data):
    region_data = defaultdict(lambda: {'sales': 0, 'count': 0})
    total = calculate_total_revenue(data)

    for t in data:
        amt = t['Quantity'] * t['UnitPrice']
        region_data[t['Region']]['sales'] += amt
        region_data[t['Region']]['count'] += 1

    result = {}
    for r, d in region_data.items():
        percent = (d['sales'] / total * 100) if total else 0
        result[r] = {
            'sales': d['sales'],
            'count': d['count'],
            'percent': round(percent, 2)
        }

    return dict(sorted(result.items(), key=lambda x: x[1]['sales'], reverse=True))


# -----------------------------------------
def top_selling_products(data, limit=5):
    prod = defaultdict(lambda: {'qty': 0, 'rev': 0})

    for t in data:
        prod[t['ProductName']]['qty'] += t['Quantity']
        prod[t['ProductName']]['rev'] += t['Quantity'] * t['UnitPrice']

    sorted_items = sorted(prod.items(), key=lambda x: x[1]['qty'], reverse=True)

    return [(n, d['qty'], d['rev']) for n, d in sorted_items[:limit]]


# -----------------------------------------
def customer_analysis(data):
    cust = defaultdict(lambda: {'spent': 0, 'orders': 0, 'products': set()})

    for t in data:
        amt = t['Quantity'] * t['UnitPrice']
        c = cust[t['CustomerID']]

        c['spent'] += amt
        c['orders'] += 1
        c['products'].add(t['ProductName'])

    result = {}
    for cid, d in cust.items():
        avg = d['spent'] / d['orders'] if d['orders'] else 0
        result[cid] = {
            'spent': d['spent'],
            'orders': d['orders'],
            'avg': round(avg, 2),
            'products': list(d['products'])
        }

    return dict(sorted(result.items(), key=lambda x: x[1]['spent'], reverse=True))


# -----------------------------------------
def daily_sales_trend(data):
    daily = defaultdict(lambda: {'sales': 0, 'count': 0, 'customers': set()})

    for t in data:
        d = daily[t['Date']]
        d['sales'] += t['Quantity'] * t['UnitPrice']
        d['count'] += 1
        d['customers'].add(t['CustomerID'])

    result = {}
    for date, d in daily.items():
        result[date] = {
            'sales': d['sales'],
            'count': d['count'],
            'unique_customers': len(d['customers'])
        }

    return dict(sorted(result.items()))


# -----------------------------------------
def find_peak_sales_day(data):
    daily = daily_sales_trend(data)
    return max(daily.items(), key=lambda x: x[1]['sales'])


# -----------------------------------------
def low_performing_products(data, limit=10):
    prod = defaultdict(lambda: {'qty': 0, 'rev': 0})

    for t in data:
        prod[t['ProductName']]['qty'] += t['Quantity']
        prod[t['ProductName']]['rev'] += t['Quantity'] * t['UnitPrice']

    low = [(n, d['qty'], d['rev']) for n, d in prod.items() if d['qty'] < limit]
    return sorted(low, key=lambda x: x[1])

# -----------------------------------------
# GENERATE SALES REPORT
# -----------------------------------------
def generate_sales_report(data, enriched_data, file_path="output/sales_report.txt"):
    import os
    from datetime import datetime

    # create output folder if not exists
    os.makedirs("output", exist_ok=True)

    total = calculate_total_revenue(data)
    total_orders = len(data)
    avg = total / total_orders if total_orders else 0

    with open(file_path, "w", encoding="utf-8") as f:

        f.write("=" * 40 + "\n")
        f.write("        SALES REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Generated: {datetime.now()}\n\n")

        f.write("SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: Rs. {total:,.2f}\n")
        f.write(f"Total Transactions: {total_orders}\n")
        f.write(f"Average Order Value: Rs. {avg:,.2f}\n\n")

        f.write("TOP PRODUCTS\n")
        f.write("-" * 40 + "\n")
        top = top_selling_products(data)
        for i, (name, qty, rev) in enumerate(top, 1):
            f.write(f"{i}. {name} | Qty: {qty} | Rs. {rev:,.2f}\n")

        f.write("\nLOW PERFORMING PRODUCTS\n")
        f.write("-" * 40 + "\n")
        low = low_performing_products(data)
        for name, qty, rev in low:
            f.write(f"{name} | Qty: {qty} | Rs. {rev:,.2f}\n")

    print("✅ Report generated:", file_path)
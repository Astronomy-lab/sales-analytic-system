# -----------------------------------------
# READ SALES DATA
# -----------------------------------------
def read_sales_data(file_path):
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as file:
                lines = file.readlines()

            # remove header + empty lines
            return [line.strip() for line in lines[1:] if line.strip()]

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print("❌ File not found:", file_path)
            return []

    print("❌ Unsupported file encoding")
    return []


# -----------------------------------------
# PARSE DATA
# -----------------------------------------
def parse_transactions(lines):
    transactions = []
    invalid_count = 0

    for line in lines:
        parts = line.split('|')

        if len(parts) != 8:
            invalid_count += 1
            continue

        try:
            transactions.append({
                'TransactionID': parts[0],
                'Date': parts[1],
                'ProductID': parts[2],
                'ProductName': parts[3].replace(',', ''),
                'Quantity': int(parts[4]),
                'UnitPrice': float(parts[5].replace(',', '')),
                'CustomerID': parts[6],
                'Region': parts[7]
            })
        except:
            invalid_count += 1

    return transactions, invalid_count


# -----------------------------------------
# VALIDATE + FILTER
# -----------------------------------------
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid = 0
    removed_region = 0
    removed_amount = 0

    for t in transactions:
        amount = t['Quantity'] * t['UnitPrice']

        # validation
        if (t['Quantity'] <= 0 or t['UnitPrice'] <= 0 or
            not t['CustomerID'] or not t['Region'] or
            not t['TransactionID'].startswith('T') or
            not t['ProductID'].startswith('P') or
            not t['CustomerID'].startswith('C')):
            invalid += 1
            continue

        # region filter
        if region and t['Region'] != region:
            removed_region += 1
            continue

        # amount filter
        if min_amount and amount < min_amount:
            removed_amount += 1
            continue

        if max_amount and amount > max_amount:
            removed_amount += 1
            continue

        valid.append(t)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid,
        'filtered_by_region': removed_region,
        'filtered_by_amount': removed_amount,
        'final_count': len(valid)
    }

    return valid, summary


# utils/file_handler.py

# This function reads a file and returns all the lines except the first (header)
def read_sales_data(filepath):
    """
    Read sales data from a file.
    Try utf-8, latin-1, and cp1252 encodings.
    Returns list of lines (without header).
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for enc in encodings:
        try:
            file = open(filepath, 'r', encoding=enc)
            lines = file.readlines()
            file.close()
            # Skip the first line because it is header
            return lines[1:]
        except UnicodeDecodeError:
            # If encoding fails, try the next one
            continue
        except FileNotFoundError:
            print("File not found: " + filepath)
            return []

    print("No encoding worked for this file.")
    return []


# This function turns raw lines into transaction dictionaries
def parse_transactions(raw_lines):
    """
    Convert each line to a dictionary with keys:
    TransactionID, Date, ProductID, ProductName, Quantity, UnitPrice, CustomerID, Region
    """
    transactions = []
    invalid_count = 0

    for line in raw_lines:
        line = line.strip()  # remove spaces and \n
        if line == "":
            continue  # skip empty lines

        parts = line.split('|')  # split by pipe symbol

        if len(parts) != 8:
            invalid_count = invalid_count + 1
            continue  # skip invalid lines

        try:
            transaction = {}
            transaction['TransactionID'] = parts[0]
            transaction['Date'] = parts[1]
            transaction['ProductID'] = parts[2]
            transaction['ProductName'] = parts[3].replace(',', '')  # remove commas
            transaction['Quantity'] = int(parts[4])
            transaction['UnitPrice'] = float(parts[5].replace(',', ''))
            transaction['CustomerID'] = parts[6]
            transaction['Region'] = parts[7]

            transactions.append(transaction)
        except:
            invalid_count = invalid_count + 1

    return transactions, invalid_count


# This function checks transactions and filters them
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Check transactions if they are valid.
    Can also filter by region and amount.
    Returns a list of valid transactions and a summary dictionary.
    """
    valid = []
    invalid = 0
    filtered_region = 0
    filtered_amount = 0

    for t in transactions:
        amount = t['Quantity'] * t['UnitPrice']

        # Check if transaction is valid
        if t['Quantity'] <= 0:
            invalid = invalid + 1
            continue
        if t['UnitPrice'] <= 0:
            invalid = invalid + 1
            continue
        if t['CustomerID'] == "":
            invalid = invalid + 1
            continue
        if t['Region'] == "":
            invalid = invalid + 1
            continue
        if t['TransactionID'][0] != "T":
            invalid = invalid + 1
            continue
        if t['ProductID'][0] != "P":
            invalid = invalid + 1
            continue
        if t['CustomerID'][0] != "C":
            invalid = invalid + 1
            continue

        # Filter by region
        if region != None:
            if t['Region'] != region:
                filtered_region = filtered_region + 1
                continue

        # Filter by minimum amount
        if min_amount != None:
            if amount < min_amount:
                filtered_amount = filtered_amount + 1
                continue

        # Filter by maximum amount
        if max_amount != None:
            if amount > max_amount:
                filtered_amount = filtered_amount + 1
                continue

        # If passed all checks, add to valid list
        valid.append(t)

    # Make summary dictionary
    summary = {}
    summary['total_input'] = len(transactions)
    summary['invalid'] = invalid
    summary['filtered_by_region'] = filtered_region
    summary['filtered_by_amount'] = filtered_amount
    summary['final_count'] = len(valid)

    return valid, summary
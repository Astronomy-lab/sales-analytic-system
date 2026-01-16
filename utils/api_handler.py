# utils/api_handler.py

import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print("API SUCCESS: Products fetched =", len(products))
        return products

    except Exception as e:
        print("API FAILED:", e)
        return []


def create_product_mapping(api_products):
    """
    Creates mapping of product ID → product info
    """
    product_map = {}

    for product in api_products:
        product_id = product.get("id")

        product_map[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_map


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product info
    """
    enriched = []

    for t in transactions:
        enriched_txn = t.copy()

        try:
            # Extract numeric part of ProductID (P101 → 101)
            pid = int(''.join(filter(str.isdigit, t['ProductID'])))

            if pid in product_mapping:
                enriched_txn['API_Category'] = product_mapping[pid]['category']
                enriched_txn['API_Brand'] = product_mapping[pid]['brand']
                enriched_txn['API_Rating'] = product_mapping[pid]['rating']
                enriched_txn['API_Match'] = True
            else:
                enriched_txn['API_Category'] = None
                enriched_txn['API_Brand'] = None
                enriched_txn['API_Rating'] = None
                enriched_txn['API_Match'] = False

        except:
            enriched_txn['API_Category'] = None
            enriched_txn['API_Brand'] = None
            enriched_txn['API_Rating'] = None
            enriched_txn['API_Match'] = False

        enriched.append(enriched_txn)

    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    with open(filename, "w", encoding="utf-8") as file:

        header = (
            "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
            "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
        )
        file.write(header)

        for t in enriched_transactions:
            line = (
                f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|"
                f"{t['ProductName']}|{t['Quantity']}|{t['UnitPrice']}|"
                f"{t['CustomerID']}|{t['Region']}|"
                f"{t.get('API_Category')}|{t.get('API_Brand')}|"
                f"{t.get('API_Rating')}|{t.get('API_Match')}\n"
            )
            file.write(line)

    print("Enriched data saved to:", filename)
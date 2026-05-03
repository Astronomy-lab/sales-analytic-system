# utils/api_handler.py

import requests


# -----------------------------------------
def fetch_all_products():
    url = "https://dummyjson.com/products?limit=100"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json().get("products", [])

    except Exception as e:
        print("❌ API Error:", e)
        return []


# -----------------------------------------
def create_product_mapping(products):
    return {
        p['id']: {
            'category': p.get('category'),
            'brand': p.get('brand'),
            'rating': p.get('rating')
        }
        for p in products
    }


# -----------------------------------------
def enrich_sales_data(data, mapping):
    enriched = []

    for t in data:
        new = t.copy()

        try:
            pid = int(t['ProductID'].replace('P', ''))

            if pid in mapping:
                new.update({
                    'API_Category': mapping[pid]['category'],
                    'API_Brand': mapping[pid]['brand'],
                    'API_Rating': mapping[pid]['rating'],
                    'API_Match': True
                })
            else:
                new['API_Match'] = False

        except:
            new['API_Match'] = False

        enriched.append(new)

    return enriched


# -----------------------------------------
def save_enriched_data(data, path="data/enriched_sales_data.txt"):
    with open(path, "w", encoding="utf-8") as f:

        header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
        f.write(header)

        for t in data:
            line = "|".join([
                str(t.get('TransactionID')),
                str(t.get('Date')),
                str(t.get('ProductID')),
                str(t.get('ProductName')),
                str(t.get('Quantity')),
                str(t.get('UnitPrice')),
                str(t.get('CustomerID')),
                str(t.get('Region')),
                str(t.get('API_Category')),
                str(t.get('API_Brand')),
                str(t.get('API_Rating')),
                str(t.get('API_Match'))
            ]) + "\n"

            f.write(line)

    print("✅ Enriched data saved:", path)

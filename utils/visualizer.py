# utils/visualizer.py

import matplotlib.pyplot as plt


# -----------------------------------------
# REGION SALES BAR CHART
# -----------------------------------------
def plot_region_sales(region_data):
    regions = list(region_data.keys())
    sales = [region_data[r]['sales'] for r in regions]

    plt.figure()
    plt.bar(regions, sales)
    plt.title("Region-wise Sales")
    plt.xlabel("Region")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.savefig("output/region_sales.png")
    plt.close()


# -----------------------------------------
# TOP PRODUCTS CHART
# -----------------------------------------
def plot_top_products(products):
    names = [p[0] for p in products]
    qty = [p[1] for p in products]

    plt.figure()
    plt.bar(names, qty)
    plt.title("Top Selling Products (Quantity)")
    plt.xlabel("Product")
    plt.ylabel("Quantity")
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.savefig("output/top_products.png")
    plt.close()


# -----------------------------------------
# DAILY SALES LINE CHART
# -----------------------------------------
def plot_daily_sales(daily_data):
    dates = list(daily_data.keys())
    revenue = [daily_data[d]['sales'] for d in dates]

    plt.figure()
    plt.plot(dates, revenue, marker='o')
    plt.title("Daily Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig("output/daily_sales.png")
    plt.close()

# -----------------------------------------
# REGION SALES PIE CHART
# -----------------------------------------
def plot_region_pie(region_data):
    import matplotlib.pyplot as plt

    labels = list(region_data.keys())
    percentages = [region_data[r]['percent'] for r in region_data]

    plt.figure()
    plt.pie(percentages, labels=labels, autopct='%1.1f%%')
    plt.title("Region-wise Sales Distribution")

    plt.tight_layout()
    plt.savefig("output/region_pie.png")
    plt.close()

# -----------------------------------------
# FULL DASHBOARD (ALL CHARTS IN ONE IMAGE)
# -----------------------------------------
def create_dashboard(region_data, top_products, daily_data):
    import matplotlib.pyplot as plt

    # Create 2x2 grid
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # ---------------- TOP LEFT: REGION BAR ----------------
    regions = list(region_data.keys())
    sales = [region_data[r]['sales'] for r in regions]

    axs[0, 0].bar(regions, sales)
    axs[0, 0].set_title("Region Sales")
    axs[0, 0].tick_params(axis='x', rotation=30)

    # ---------------- TOP RIGHT: PIE ----------------
    percentages = [region_data[r]['percent'] for r in region_data]

    axs[0, 1].pie(percentages, labels=regions, autopct='%1.1f%%')
    axs[0, 1].set_title("Region Distribution")

    # ---------------- BOTTOM LEFT: TOP PRODUCTS ----------------
    names = [p[0] for p in top_products]
    qty = [p[1] for p in top_products]

    axs[1, 0].bar(names, qty)
    axs[1, 0].set_title("Top Products")
    axs[1, 0].tick_params(axis='x', rotation=30)

    # ---------------- BOTTOM RIGHT: DAILY TREND ----------------
    dates = list(daily_data.keys())
    revenue = [daily_data[d]['sales'] for d in dates]

    axs[1, 1].plot(dates, revenue, marker='o')
    axs[1, 1].set_title("Daily Sales Trend")
    axs[1, 1].tick_params(axis='x', rotation=45)

    # Layout fix
    plt.tight_layout()

    # Save image
    import os
    os.makedirs("output", exist_ok=True)
    plt.savefig("output/dashboard.png")

    plt.close()

    print("✅ Dashboard created: output/dashboard.png")
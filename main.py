# -------- FILE HANDLING --------
from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

# -------- DATA PROCESSING / ANALYTICS --------
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    low_performing_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    generate_sales_report
)

# -------- API INTEGRATION --------
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


def main():
    try:
        print("=" * 40)
        print("      SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # ------------------ STEP 1 ------------------
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f" Successfully read {len(raw_lines)} transactions")

        # ------------------ STEP 2 ------------------
        print("\n[2/10] Parsing and cleaning data...")
        transactions, parse_invalid = parse_transactions(raw_lines)
        print(f" Parsed {len(transactions)} records")
        if parse_invalid:
            print(f"⚠ Ignored {parse_invalid} invalid rows")

        # ------------------ STEP 3 ------------------
        print("\n[3/10] Filter Options Available:")
        regions = sorted(set(t['Region'] for t in transactions))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]

        print("Regions:", ", ".join(regions))
        print(f"Amount Range: Rs. {min(amounts):,.0f} - Rs. {max(amounts):,.0f}")

        choice = input("Do you want to filter data? (y/n): ").lower()

        if choice == 'y':
            region = input("Enter region (or press Enter to skip): ").strip() or None
            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amt = float(min_amt) if min_amt else None
            max_amt = float(max_amt) if max_amt else None

            valid_data, summary = validate_and_filter(
                transactions,
                region=region,
                min_amount=min_amt,
                max_amount=max_amt
            )
        else:
            valid_data, summary = validate_and_filter(transactions)

        # ------------------ STEP 4 ------------------
        print("\n[4/10] Validating transactions...")
        print(f" Valid: {summary['final_count']} | Invalid: {summary['invalid']}")

        # ------------------ STEP 5 ------------------
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_data)
        region_wise_sales(valid_data)
        top_selling_products(valid_data)
        low_performing_products(valid_data)
        customer_analysis(valid_data)
        daily_sales_trend(valid_data)
        find_peak_sales_day(valid_data)
        print(" Analysis complete")

        # ------------------ STEP 6 ------------------
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f" Fetched {len(api_products)} products")

        # ------------------ STEP 7 ------------------
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_data, product_mapping)

        enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
        rate = (enriched_count / len(valid_data)) * 100 if valid_data else 0
        print(f" Enriched {enriched_count}/{len(valid_data)} transactions ({rate:.1f}%)")

        # ------------------ STEP 8 ------------------
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print(" Saved to: data/enriched_sales_data.txt")

        # ------------------ STEP 9 ------------------
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_data, enriched_transactions)
        print(" Report saved to: output/sales_report.txt")

        # ------------------ STEP 10 ------------------
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n ERROR OCCURRED")
        print("Reason:", e)
        print("Please check file paths and data format.")
        print("=" * 40)


# Run program
if __name__ == "__main__":
    main()




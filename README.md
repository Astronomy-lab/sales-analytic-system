# Sales Analytics System (made by Aditya Vikram Singh)

## About Assignment

This is a simple **Sales Analytics System** made using Python.
This assignment is created for **students and beginners** who are learning Python, file handling, dictionary, list, and API concept.

The main work of this assignment is to:

* Read sales data from a file
* Clean and validate data
* Do sales analysis
* Use API to get product details
* Generate final report

This assignment is **not very advance**, it is written in easy way so beginner can understand.

---

## Folder Structure

```
sales-analytics-system/<br>
│
├── data/<br>
│   ├── sales_data.txt<br>
│   └── enriched_sales_data.txt<br>
│
├── output/<br>
│   └── sales_report.txt<br>
│
├── utils/<br>
│   ├── file_handler.py<br>
│   ├── data_processor.py<br>
│   └── api_handler.py<br>
│
├── main.py<br>
└── README.md<br>
```

---

## Files Explanation

### 1. file_handler.py

This file is used for **reading and cleaning sales file**.

Functions inside this file:

* `read_sales_data()` – reads data from text file<br>
* `parse_transactions()` – converts raw lines into dictionary<br>
* `validate_and_filter()` – remove invalid data and filter by region or amount<br>

This file mostly work with **file handling** and **string split**.<br>

---

### 2. data_processor.py

This file do all **calculation and analysis**.

Functions included:

* Calculate total revenue
* Region wise sales
* Top selling products
* Low performing products
* Customer analysis
* Daily sales trend
* Peak sales day
* Generate final report

All logic is written in very simple way using loops and dictionary.

---

### 3. api_handler.py

This file connect sales data with **DummyJSON API**.

Work of this file:

* Fetch product list from API
* Match ProductID with API product id
* Add category, brand and rating in sales data
* Save enriched data in file

This help to understand **basic API calling using requests module**.

---

### 4. main.py

This is the **main program file**.

This file do following steps:

1. Read sales data
2. Parse and clean data
3. Ask user for filter option
4. Do analysis
5. Fetch API data
6. Enrich sales data
7. Save enriched file
8. Generate report

All steps are printed so user can understand what is happening.

---

## How to Run Project

### Step 1: Install Python

Make sure Python is installed.

Check version:

```
python --version
```

### Step 2: Install Required Module

This project need only one external module:

```
pip install requests
```

### Step 3: Run Program

Go to assignment folder and run:

```
python main.py
```

---

## Output Files

* `data/enriched_sales_data.txt` → Sales data with API details
* `output/sales_report.txt` → Final analytics report

---

## Learning Outcome

After completing this project, I learn:

* File reading and writing
* Dictionary and list usage
* Data validation
* Basic analytics logic
* API integration
* Writing clean beginner level code

---

Thank you 😊



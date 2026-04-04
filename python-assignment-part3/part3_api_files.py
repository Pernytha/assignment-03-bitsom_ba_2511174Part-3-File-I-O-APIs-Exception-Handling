#Product Explorer & Error-Resilient Logger

import requests
from datetime import datetime
import os
from pathlib import Path

script_dir = Path(__file__).parent

print("Script folder:" ,script_dir)
print("Current working directory:",Path.cwd())






#TASK 1 — FILE OPERATIONS


def task1_file_operation():
    filename = os.path.join(script_dir,"python_notes.txt")

    # Part A — Write
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Topic 1: Variables store data. Python is dynamically typed.\n")
            f.write("Topic 2: Lists are ordered and mutable.\n")
            f.write("Topic 3: Dictionaries store key-value pairs.\n")
            f.write("Topic 4: Loops automate repetitive tasks.\n")
            f.write("Topic 5: Exception handling prevents crashes.\n")
        print("File written successfully.")
    except Exception as e:
        print("Error writing file:", e)

    # Append lines
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write("Topic 6: Functions help reuse code.\n")
            f.write("Topic 7: APIs allow communication between systems.\n")
        print("Lines appended.")
    except Exception as e:
        print("Error appending file:", e)

    # Part B — Read
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        print("\n--- File Content ---")
        for i, line in enumerate(lines, start=1):
            print(f"{i}. {line.strip()}")

        print("Total lines:", len(lines))

        keyword = input("\nEnter keyword to search: ").lower()
        found = False

        for l in lines:
            if keyword in l.lower():
                print(line.strip())
                found = True

        if not found:
            print("No matching lines found.")

    except Exception as e:
        print("Error reading file:", e)





def log_error(function_name, error_type, message):
    log_file = os.path.join(script_dir,"error_log.txt")
    with open(log_file, "a", encoding="utf-8") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] ERROR in {function_name}: {error_type} — {message}\n")



#TASK 2 — API INTEGRATION


BASE_URL = "https://dummyjson.com/products"

def fetch_products():
    try:
        response = requests.get(f"{BASE_URL}?limit=20", timeout=5)
        response.raise_for_status()
        return response.json()["products"]

    except requests.exceptions.ConnectionError:
        print("Connection failed.")
        log_error("fetch_products", "ConnectionError", "No connection")
    except requests.exceptions.Timeout:
        print("Request timed out.")
        log_error("fetch_products", "Timeout", "Server too slow")
    except Exception as e:
        print("Error:", e)
        log_error("fetch_products", "Exception", str(e))

    return []


def display_products(products):
    print("\nID | Title | Category | Price | Rating")
    print("-" * 60)

    for p in products:
        print(f"{p['id']} | {p['title'][:20]} | {p['category']} | ${p['price']} | {p['rating']}")


def filter_sort_products(products):
    filtered = [p for p in products if p["rating"] >= 4.5]
    sorted_products = sorted(filtered, key=lambda x: x["price"], reverse=True)

    print("\nFiltered & Sorted Products:")
    for p in sorted_products:
        print(f"{p['title']} - ${p['price']} (Rating: {p['rating']})")


def fetch_laptops():
    try:
        response = requests.get(f"{BASE_URL}/category/laptops", timeout=5)
        response.raise_for_status()
        data = response.json()

        print("\nLaptops:")
        for p in data["products"]:
            print(f"{p['title']} - ${p['price']}")

    except Exception as e:
        print("Error fetching laptops:", e)
        log_error("fetch_laptops", "Exception", str(e))


def create_product():
    try:
        payload = {
            "title": "My Custom Product",
            "price": 999,
            "category": "electronics",
            "description": "A product I created via API"
        }

        response = requests.post(f"{BASE_URL}/add", json=payload, timeout=5)
        print("\nPOST Response:")
        print(response.json())

    except Exception as e:
        print("Error in POST:", e)
        log_error("create_product", "Exception", str(e))



#TASK 3 — EXCEPTION HANDLING



def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"



def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")



def product_lookup():
    while True:
        user_input = input("\nEnter product ID (1–100) or 'quit': ")

        if user_input.lower() == "quit":
            break

        if not user_input.isdigit():
            print("Invalid input. Enter a number.")
            continue

        product_id = int(user_input)

        if not (1 <= product_id <= 100):
            print("ID must be between 1 and 100.")
            continue

        try:
            response = requests.get(f"{BASE_URL}/{product_id}", timeout=5)

            if response.status_code == 404:
                print("Product not found.")
                log_error("lookup_product", "HTTPError", f"404 for ID {product_id}")
            elif response.status_code == 200:
                data = response.json()
                print(f"{data['title']} - ${data['price']}")

        except requests.exceptions.ConnectionError:
            print("Connection failed.")
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except Exception as e:
            print("Error:", e)



#TASK 4 — ERROR LOGGING


def trigger_errors():
    # Connection error
    try:
        requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
    except Exception as e:
        log_error("test_connection", "ConnectionError", str(e))

    # HTTP error (404)
    try:
        response = requests.get(f"{BASE_URL}/999", timeout=5)
        if response.status_code != 200:
            log_error("lookup_product", "HTTPError", "404 Not Found for product ID 999")
    except Exception as e:
        log_error("lookup_product", "Exception", str(e))


def show_logs():
    try:
        log_file = os.path.join(script_dir,"error_log.txt")
        with open(log_file, "r", encoding="utf-8") as f:
            print("\n--- Error Log ---")
            print(f.read())
    except FileNotFoundError:
        print("No log file found.")



# MAIN EXECUTION

def main():
    # Task 1
    task1_file_operation()

    # Task 2
    products = fetch_products()
    display_products(products)
    filter_sort_products(products)
    fetch_laptops()
    create_product()

    # Task 3
    print("\nSafe Divide Tests:")
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    print(safe_divide("ten", 2))

    print("\nRead File Safe:")
    print(read_file_safe("python_notes.txt"))
    read_file_safe("ghost_file.txt")

    product_lookup()

    # Task 4
    trigger_errors()
    show_logs()


if __name__ == "__main__":
    main()

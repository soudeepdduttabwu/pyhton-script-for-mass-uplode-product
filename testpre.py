import tkinter as tk
from datetime import datetime
import pandas as pd

def get_meta_data(category_id):
    meta_data_map = {
        "1": {"meta_title": "Tractor", "meta_description": "Buy and Sell Used Tractors"},
        "3": {"meta_title": "Goods Vehicle", "meta_description": "Buy and Sell Used Goods Vehicles"},
        "4": {"meta_title": "Harvester", "meta_description": "Buy and Sell Used Harvesters"},
        "5": {"meta_title": "Implements", "meta_description": "Buy and Sell Agricultural Implements"},
        "6": {"meta_title": "Seeds", "meta_description": "Buy and Sell Agricultural Seeds"},
        "7": {"meta_title": "Tyres", "meta_description": "Buy and Sell Agricultural Tyres"},
        "8": {"meta_title": "Pesticides", "meta_description": "Buy and Sell Agricultural Pesticides"},
        "9": {"meta_title": "Fertilizers", "meta_description": "Buy and Sell Agricultural Fertilizers"},
    }
    return meta_data_map.get(category_id, {"meta_title": "Product", "meta_description": "Buy and Sell Products"})

def generate_sql_insert_statement(data, last_id):
    next_id = last_id + 1
    meta_data = get_meta_data(data['category_id']) 

    sql = f"""
    INSERT INTO krishivikas_kvlive.tractor (
        id, category_id, user_id, set, type, brand_id, model_id, year_of_purchase, 
        title, rc_available, noc_available, registration_no, description, price, 
        is_negotiable, country_id, state_id, district_id, city_id, pincode, 
        latlong, status, slug, meta_title, meta_description, created_at, updated_at
    ) VALUES (
        '{next_id}', '{data['category_id']}', '{data['user_id']}', 'sell', 'new', 
        '{data['brand_id']}', '{data['model_id']}', '{data['year_of_purchase']}', 
        '{data['title']}', '0', '0', 'NA', '{data['description']}', '{data['price']}', 
        '1', '1', '{data['state_id']}', '{data['district_id']}', '{data['city_id']}', 
        '{data['pincode']}', '{data['latlong']}', '0', 'tractor', 
        '{meta_data['meta_title']}', '{meta_data['meta_description']}', 
        '{data['created_at']}', '{data['created_at']}'
    );
    """
    return sql

def process_excel_data(file_path, user_data, last_primary_key):
    try:
        df = pd.read_excel(file_path)
        sql_statements = []
        current_id = int(last_primary_key)  # Convert last primary key to integer

        for index, row in df.iterrows():
            try:
                data = {
                    **user_data,
                    "title": row['Product name'], 
                    "description": row['Description'], 
                    "price": str(row['Price']), 
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                }
                sql_statement = generate_sql_insert_statement(data, current_id)
                sql_statements.append(sql_statement)
                current_id += 1  # Increment for the next record
            except KeyError as e:
                print(f"Error: Column '{e.args[0]}' not found in Excel file.")
                continue

        with open("sql_queries.txt", "w") as f:
            for sql in sql_statements:
                f.write(sql + "\n")

        return sql_statements
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return []

def submit_and_display():
    try:
        file_path = "Book1.xlsx"
        user_data = {
            "user_id": user_id_entry.get(),
            "category_id": category_id_entry.get(),
            "brand_id": brand_id_entry.get(),
            "model_id": model_id_entry.get(),
            "year_of_purchase": year_of_purchase_entry.get(),
            "city_id": city_id_entry.get(),
            "state_id": state_id_entry.get(),
            "district_id": district_id_entry.get(),
            "pincode": pincode_entry.get(),
            "latlong": latlong_entry.get(),
        }
        last_primary_key = last_id_entry.get()
        sql_statements = process_excel_data(file_path, user_data, last_primary_key)

        if sql_statements:
            result_label.config(text="SQL statements saved to sql_queries.txt")
        else:
            result_label.config(text="No SQL statements generated.")
    except FileNotFoundError:
        result_label.config(text="Excel file not found.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# Create the main window
window = tk.Tk()
window.title("Tractor Data Entry from Excel")

tk.Label(window, text="User ID:").grid(row=0, column=0, sticky="e")
user_id_entry = tk.Entry(window)
user_id_entry.grid(row=0, column=1)

tk.Label(window, text="Category ID:").grid(row=1, column=0, sticky="e")
category_id_entry = tk.Entry(window)
category_id_entry.grid(row=1, column=1)

tk.Label(window, text="Brand ID:").grid(row=2, column=0, sticky="e")
brand_id_entry = tk.Entry(window)
brand_id_entry.grid(row=2, column=1)

tk.Label(window, text="Model ID:").grid(row=3, column=0, sticky="e")
model_id_entry = tk.Entry(window)
model_id_entry.grid(row=3, column=1)

tk.Label(window, text="Year of Purchase:").grid(row=4, column=0, sticky="e")
year_of_purchase_entry = tk.Entry(window)
year_of_purchase_entry.grid(row=4, column=1)

tk.Label(window, text="City ID:").grid(row=5, column=0, sticky="e")
city_id_entry = tk.Entry(window)
city_id_entry.grid(row=5, column=1)

tk.Label(window, text="State ID:").grid(row=6, column=0, sticky="e")
state_id_entry = tk.Entry(window)
state_id_entry.grid(row=6, column=1)

tk.Label(window, text="District ID:").grid(row=7, column=0, sticky="e")
district_id_entry = tk.Entry(window)
district_id_entry.grid(row=7, column=1)

tk.Label(window, text="Pincode:").grid(row=8, column=0, sticky="e")
pincode_entry = tk.Entry(window)
pincode_entry.grid(row=8, column=1)

tk.Label(window, text="LatLong:").grid(row=9, column=0, sticky="e")
latlong_entry = tk.Entry(window)
latlong_entry.grid(row=9, column=1)

tk.Label(window, text="Last Primary Key:").grid(row=10, column=0, sticky="e")
last_id_entry = tk.Entry(window)
last_id_entry.grid(row=10, column=1)

submit_button = tk.Button(window, text="Process Excel", command=submit_and_display)
submit_button.grid(row=11, column=0, columnspan=2)

result_label = tk.Label(window, text="")
result_label.grid(row=12, column=0, columnspan=2)

window.mainloop()

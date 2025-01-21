import tkinter as tk
from datetime import datetime
import pandas as pd
import os

def get_meta_data(category_id):
  """
  Determines meta_title and meta_description based on category_id.

  Args:
    category_id: The category ID.

  Returns:
    A dictionary containing meta_title and meta_description.
  """
  if category_id == "1":
    return {"meta_title": "Tractor", "meta_description": "Buy and Sell Used Tractors"}
  elif category_id == "3":
    return {"meta_title": "Goods Vehicle", "meta_description": "Buy and Sell Used Goods Vehicles"}
  elif category_id == "4":
    return {"meta_title": "Harvester", "meta_description": "Buy and Sell Used Harvesters"}
  elif category_id == "5":
    return {"meta_title": "Implements", "meta_description": "Buy and Sell Agricultural Implements"}
  elif category_id == "6":
    return {"meta_title": "Seeds", "meta_description": "Buy and Sell Agricultural Seeds"}
  elif category_id == "7":
    return {"meta_title": "Tyres", "meta_description": "Buy and Sell Agricultural Tyres"}
  elif category_id == "8":
    return {"meta_title": "Pesticides", "meta_description": "Buy and Sell Agricultural Pesticides"}
  elif category_id == "9":
    return {"meta_title": "Fertilizers", "meta_description": "Buy and Sell Agricultural Fertilizers"}
  else:
    return {"meta_title": "Product", "meta_description": "Buy and Sell Products"}

def generate_sql_insert_statement(data, last_id):
  """
  Generates an SQL INSERT statement based on the provided data.

  Args:
    data: A dictionary containing the user-provided values.
    last_id: The last primary key value.

  Returns:
    An SQL INSERT statement.
  """
  next_id = last_id + 1  # Calculate the next ID
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
      '{data['pincode']}', '{data['latlong']}', '1', 'tractor', 
      '{meta_data['meta_title']}', '{meta_data['meta_description']}', 
      '{data['created_at']}', '{data['created_at']}'
  );
  """
  return sql

def process_excel_data(file_path):
  """
  Reads data from the Excel file and generates SQL statements.

  Args:
    file_path: Path to the Excel file.

  Returns:
    A list of SQL statements.
  """
  try:
    df = pd.read_excel(file_path)
    sql_statements = []
    for index, row in df.iterrows():
      try:
        data = {
            "user_id": "Your_User_ID",  # Replace with actual user ID
            "category_id": "1",  # Assuming 'Tractor' is category 1
            "brand_id": "1",  # Replace with actual brand ID based on logic
            "model_id": "1",  # Replace with actual model ID based on logic
            "year_of_purchase": "2023",  # Replace with actual year of purchase 
            "city_id": "1",  # Replace with actual city ID
            "state_id": "1",  # Replace with actual state ID
            "district_id": "1",  # Replace with actual district ID
            "pincode": "123456",  # Replace with actual pincode 
            "latlong": "28.6139,77.2090",  # Replace with actual latlong 
            "title": row['Product name'], 
            "description": row['Description'], 
            "price": str(row['Price']), 
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Generate current timestamp
        }
        last_id = index + 1  # Assuming ID starts from 1
        sql_statement = generate_sql_insert_statement(data, last_id)
        sql_statements.append(sql_statement)
      except KeyError as e:
        print(f"Error: Column '{e.args[0]}' not found in Excel file.") 
        continue  # Skip the row if the column is missing

    # Save SQL statements to a text file
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

# ... (Rest of the GUI code remains the same)

def submit_and_display():
  """
  Handles the button click event.
  """
  file_path = "Book1.xlsx"  # Replace with actual file name
  sql_statements = process_excel_data(file_path)

  if sql_statements:
    result_label.config(text="SQL statements saved to sql_queries.txt")
  else:
    result_label.config(text="No SQL statements generated.")

# Create the main window
window = tk.Tk()
window.title("Tractor Data Entry from Excel")

# ... (Create labels and entry fields as before - these are not used for Excel data)

# Create the submit button
submit_button = tk.Button(window, text="Process Excel", command=submit_and_display)
submit_button.grid(row=11, column=0, columnspan=2)

# Create a label to display the result
result_label = tk.Label(window, text="")
result_label.grid(row=12, column=0, columnspan=2)

# Run the main event loop
window.mainloop()
import tkinter as tk
from datetime import datetime

def get_user_input():
  """
  Gets user input from the GUI and returns a dictionary.

  Returns:
    A dictionary containing the user-provided values.
  """
  user_id = user_id_entry.get()
  category_id = category_id_entry.get()
  brand_id = brand_id_entry.get()
  model_id = model_id_entry.get()
  year_of_purchase = year_of_purchase_entry.get()
  city_id = city_id_entry.get()
  state_id = state_id_entry.get()
  district_id = district_id_entry.get()
  pincode = pincode_entry.get()
  latlong = latlong_entry.get()
  created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  return {
      "user_id": user_id,
      "category_id": category_id,
      "brand_id": brand_id,
      "model_id": model_id,
      "year_of_purchase": year_of_purchase,
      "city_id": city_id,
      "state_id": state_id,
      "district_id": district_id,
      "pincode": pincode,
      "latlong": latlong,
      "created_at": created_at
  }

def get_meta_data(category_id):
  """
  Determines meta_title and meta_description based on category_id.

  Args:
    category_id: The category ID.

  Returns:
    A dictionary containing meta_title and meta_description.
  """
  if category_id == "1":
    return {"meta_title": "Tractor", "meta_description": " Sell new Tractors"}
  elif category_id == "3":
    return {"meta_title": "Goods Vehicle", "meta_description": "Sell new Goods Vehicles"}
  elif category_id == "4":
    return {"meta_title": "Harvester", "meta_description": "Sell new Harvesters"}
  elif category_id == "5":
    return {"meta_title": "Implements", "meta_description": "Sell new Agricultural Implements"}
  elif category_id == "6":
    return {"meta_title": "Seeds", "meta_description": " Sell Agricultural Seeds"}
  elif category_id == "7":
    return {"meta_title": "Tyres", "meta_description": " Sell Agricultural Tyres"}
  elif category_id == "8":
    return {"meta_title": "Pesticides", "meta_description": " Sell Agricultural Pesticides"}
  elif category_id == "9":
    return {"meta_title": "Fertilizers", "meta_description": "Sell Agricultural Fertilizers"}
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
      'Tractor', '0', '0', 'NA', '', '0', '1', '1', 
      '{data['state_id']}', '{data['district_id']}', '{data['city_id']}', 
      '{data['pincode']}', '{data['latlong']}', '1', 'tractor', 
      '{meta_data['meta_title']}', '{meta_data['meta_description']}', 
      '{data['created_at']}', '{data['created_at']}'
  );
  """
  return sql

def submit_and_display():
  """
  Handles the button click event.
  """
  try:
    last_id = int(last_id_entry.get())  # Get last ID from the user input
  except ValueError:
    result_label.config(text="Invalid Last ID. Please enter an integer.")
    return

  user_data = get_user_input()
  sql_statement = generate_sql_insert_statement(user_data, last_id)
  result_label.config(text="Generated SQL:\n" + sql_statement)

# Create the main window
window = tk.Tk()
window.title("Tractor Data Entry")

# Create labels and entry fields
user_id_label = tk.Label(window, text="User ID:")
user_id_label.grid(row=0, column=0)
user_id_entry = tk.Entry(window)
user_id_entry.grid(row=0, column=1)

category_id_label = tk.Label(window, text="Category ID:")
category_id_label.grid(row=1, column=0)
category_id_entry = tk.Entry(window)
category_id_entry.grid(row=1, column=1)

brand_id_label = tk.Label(window, text="Brand ID:")
brand_id_label.grid(row=2, column=0)
brand_id_entry = tk.Entry(window)
brand_id_entry.grid(row=2, column=1)

model_id_label = tk.Label(window, text="Model ID:")
model_id_label.grid(row=3, column=0)
model_id_entry = tk.Entry(window)
model_id_entry.grid(row=3, column=1)

year_of_purchase_label = tk.Label(window, text="Year of Purchase:")
year_of_purchase_label.grid(row=4, column=0)
year_of_purchase_entry = tk.Entry(window)
year_of_purchase_entry.grid(row=4, column=1)

city_id_label = tk.Label(window, text="City ID:")
city_id_label.grid(row=5, column=0)
city_id_entry = tk.Entry(window)
city_id_entry.grid(row=5, column=1)

state_id_label = tk.Label(window, text="State ID:")
state_id_label.grid(row=6, column=0)
state_id_entry = tk.Entry(window)
state_id_entry.grid(row=6, column=1)

district_id_label = tk.Label(window, text="District ID:")
district_id_label.grid(row=7, column=0)
district_id_entry = tk.Entry(window)
district_id_entry.grid(row=7, column=1)

pincode_label = tk.Label(window, text="Pincode:")
pincode_label.grid(row=8, column=0)
pincode_entry = tk.Entry(window)
pincode_entry.grid(row=8, column=1)

latlong_label = tk.Label(window, text="Latlong:")
latlong_label.grid(row=9, column=0)
latlong_entry = tk.Entry(window)
latlong_entry.grid(row=9, column=1)

last_id_label = tk.Label(window, text="Last ID:")
last_id_label.grid(row=10, column=0)
last_id_entry = tk.Entry(window)
last_id_entry.grid(row=10, column=1)

# Create the submit button
submit_button = tk.Button(window, text="Submit", command=submit_and_display)
submit_button.grid(row=11, column=0, columnspan=2)

# Create a label to display the generated SQL
result_label = tk.Label(window, text="")
result_label.grid(row=12, column=0, columnspan=2)

# Run the main event loop
window.mainloop()
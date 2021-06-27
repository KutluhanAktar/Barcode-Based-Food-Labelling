# Barcode Based Nutrient Profiling and Food Labelling w/ TensorFlow
#
# Windows, Linux, or Ubuntu
#
# By Kutluhan Aktar
#
# Collect nutrition facts by barcodes to distinguish healthy and unhealthy foods w/ a neural network model predicting Nutri-Score classes. 
#
#
# For more information:
# https://www.theamplituhedron.com/projects/Barcode-Based-Nutrient-Profiling-and-Food-Labelling-w-TensorFlow

import json
from time import sleep
import requests
from csv import writer
from product_barcode_list import product_barcode_list

class create_database:
    def __init__(self, server):
        self.server = server
        self.product_info = 0
    # Get information from the PHP web application with the given product barcode.
    def get_information_by_barcode(self, barcode):
        data = requests.get(self.server + "?barcode=" + barcode)
        # If incoming data:
        if not (data.text == ""):
            d = json.loads(data.text)
            self.product_data = [barcode, d["quantity"], d["serving_quantity"], d["energy-kcal_100g"], d["carbohydrates_100g"], d["sugars_100g"], d["fat_100g"], d["saturated-fat_100g"], d["fruits_vegetables_100g"], d["fiber_100g"], d["proteins_100g"], d["salt_100g"], d["sodium_100g"], d["calcium_100g"], d["nutri_score"], d["nutri_grade"], d["co2_total"], d["ef_total"]]
    # List the product information depending on the given barcode list to create the database (CSV).
    def list_product_information_as_CSV(self, barcode_list):
        i = 0;
        l = len(barcode_list)
        for product_barcode in barcode_list:
            # Fetch data for each product:
            self.get_information_by_barcode(product_barcode)
            # Insert data to the CSV file for each product:
            with open("product_database.csv", "a", newline="") as f:
                # Add a new row with the product information to the file:
                writer(f).writerow(self.product_data)
                f.close()
            # Print the remaining rows:
            i+=1
            print("Fetching data... (" + str(i) + " / " + str(l) + ")")
            sleep(0.2)
        print("!!! Database created successfully !!!")

# Define a new class object named 'database':
database = create_database("http://192.168.1.20/Barcode_Product_Scanner/")

# Create the database with the product barcode list:
database.list_product_information_as_CSV(product_barcode_list)

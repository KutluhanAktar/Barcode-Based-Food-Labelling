# Barcode Based Nutrient Profiling and Food Labelling w/ TensorFlow
#
# Raspberry Pi 4 Model B
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
import numpy as np
import tensorflow as tf

class barcode_food_labelling:
    def __init__(self, server):
        self.server = server
        self.product_data = 0
        # Define class names for each Nutri-Score (food health category) classes based on nutrient profiling.
        self.nutri_score_class_names = ["Nutritious", "Healthy", "Less Healthy", "Unhealthy"]
    # Get information from the PHP web application with the given product barcode.
    def get_information_by_barcode(self, barcode):
        data = requests.get(self.server + "?barcode=" + barcode)
        # If incoming data:
        if not (data.text == ""):
            self.product_data = json.loads(data.text)
            return True
        else:
            print("\r\nBarcode Not Found!!!")
            return False
    # Format the incoming product information to create the input data for the model.
    def format_incoming_data(self):
        if not(self.product_data == 0):
            # Information:
            self.name = self.product_data["name"]
            self.type = self.product_data["type"]
            self.quantity = str(self.product_data["quantity"]) + " / " + str(self.product_data["serving_quantity"])
            # Data:
            self.energy = self.product_data["energy-kcal_100g"] / 1000
            self.carbohydrates = self.product_data["carbohydrates_100g"] / 100
            self.sugars = self.product_data["sugars_100g"] / 100
            self.fat = self.product_data["fat_100g"] / 100
            self.saturated = self.product_data["saturated-fat_100g"] / 100
            self.fiber = self.product_data["fiber_100g"] / 10
            self.proteins = self.product_data["proteins_100g"] / 100
            self.salt = self.product_data["salt_100g"] / 10
            self.sodium = self.product_data["sodium_100g"] / 10
    # Load the TensorFlow Lite model to predict the Nutri-Score class of the given food product by barcode.
    def run_TensorFlow_Lite_model(self, path):
        # Load the TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(model_path=path)
        interpreter.allocate_tensors()
        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        # Run the model with the formatted input data:
        input_data = np.array([[self.energy, self.carbohydrates, self.sugars, self.fat, self.saturated, self.fiber, self.proteins, self.salt, self.sodium]], dtype=np.float32)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        # Get output data (label): 
        output_data = interpreter.get_tensor(output_details[0]['index'])
        prediction = self.nutri_score_class_names[np.argmax(output_data)]
        print("\r\n--------------\r\n")
        print("Product => " + self.name + " " + self.type)
        print("Quantity => " + self.quantity)
        print()
        print("Prediction => " + prediction)
        print("\r\n--------------\r\n")

# Define a new class object named 'new_product':
new_product = barcode_food_labelling("http://192.168.1.20/Barcode_Product_Scanner/")

while True:
    # Get barcodes from the barcode scanner:
    barcode = input("\r\nWaiting for reading new barcodes...\r\n")
    # If successful:
    if(barcode.find("K19") < 0):
        if (new_product.get_information_by_barcode(barcode)):
            new_product.format_incoming_data()
            new_product.run_TensorFlow_Lite_model("ANN_Nutrient_Profiling.tflite")

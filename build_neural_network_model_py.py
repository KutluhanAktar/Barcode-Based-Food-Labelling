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

import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create a class to build a neural network after getting, visualizing, and scaling (normalizing) the product information data set (nutrient levels, nutrition facts, etc.).
class Nutrient_Profiling:
    def __init__(self, data):
        self.df = data
        self.inputs = []
        self.labels = []
    # Create graphics for requested columns.
    def graphics(self, column_1, column_2, x_label, y_label):
        # Show requested columns from the data set:
        plt.style.use("dark_background")
        plt.gcf().canvas.set_window_title('Barcode Based Nutrient Profiling')
        plt.hist2d(self.df[column_1], self.df[column_2], cmap='RdBu')
        plt.colorbar()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(x_label)
        plt.show()
    # Visualize data before creating and feeding the neural network model.
    def data_visualization(self):
        # Scrutinize requested columns to build a model with appropriately formatted data:
        self.graphics('carbohydrates_100g', 'energy-kcal_100g', 'Carbohydrates (g)', 'Energy (kcal)')
        self.graphics('sugars_100g', 'energy-kcal_100g', 'Sugars (g)', 'Energy (kcal)')
        self.graphics('fat_100g', 'energy-kcal_100g', 'Fat (g)', 'Energy (kcal)')
        self.graphics('saturated-fat_100g', 'energy-kcal_100g', 'Saturated fat (g)', 'Energy (kcal)')
        self.graphics('fruits_vegetables_100g', 'energy-kcal_100g', 'Fruits vegetables nuts estimate (%)', 'Energy (kcal)')
        self.graphics('fiber_100g', 'energy-kcal_100g', 'Fiber (g)', 'Energy (kcal)')
        self.graphics('proteins_100g', 'energy-kcal_100g', 'Proteins (g)', 'Energy (kcal)')
        self.graphics('salt_100g', 'energy-kcal_100g', 'Salt (g)', 'Energy (kcal)')
        self.graphics('sodium_100g', 'energy-kcal_100g', 'Sodium (g)', 'Energy (kcal)')
    # Assign labels for each product according to the nutrient-profiling model (altered).
    def define_and_assign_labels(self):
        l = len(self.df)
        for i in range(l):
            # Calculate the Nutri-Score value (altered).
            nutri_score = df["nutri_score"][i]
            calcium = df["calcium_100g"][i] * 1000
            co2 = df["co2_total"][i]
            ef = df["ef_total"][i]
            # Calcium:
            if(calcium > 110):
                nutri_score-=1
            elif(calcium > 300):
                nutri_score-=2
            # CO2 (Environmental impact):
            if(co2 > 1 and co2 <= 3):
                nutri_score+=1
            elif(co2 > 3 and co2 <= 5):
                nutri_score+=2
            elif(co2 > 5):
                nutri_score+=3
            # EF (Ecological footprint):
            if(ef > 0.2 and ef <= 0.4):
                nutri_score+=1
            elif(ef > 0.4 and ef <= 0.9):
                nutri_score+=2
            elif(ef > 0.9):
                nutri_score+=3
            # Assign classes (labels) depending on the Nutri-Score value:
            _class = 0
            if(nutri_score <= 3):
                _class = 0
            elif(nutri_score > 3 and nutri_score <= 11):
                _class = 1
            elif(nutri_score > 11 and nutri_score <= 21):
                _class = 2
            elif(nutri_score > 21):
                _class = 3
            self.labels.append(_class)
        self.labels = np.asarray(self.labels)
    # Scale (normalize) data depending on the neural network model and define inputs.
    def scale_data_and_define_inputs(self):
        self.df["scaled_energy"] = self.df.pop("energy-kcal_100g") / 1000
        self.df["scaled_carbohydrates"] = self.df.pop("carbohydrates_100g") / 100
        self.df["scaled_sugars"] = self.df.pop("sugars_100g") / 100
        self.df["scaled_fat"] = self.df.pop("fat_100g") / 100
        self.df["scaled_saturated"] = self.df.pop("saturated-fat_100g") / 100
        self.df["scaled_fiber"] = self.df.pop("fiber_100g") / 10
        self.df["scaled_proteins"] = self.df.pop("proteins_100g") / 100
        self.df["scaled_salt"] = self.df.pop("salt_100g") / 10
        self.df["scaled_sodium"] = self.df.pop("sodium_100g") / 10
        # Create the inputs array using the scaled variables:
        for i in range(len(self.df)):
            self.inputs.append(np.array([self.df["scaled_energy"][i], self.df["scaled_carbohydrates"][i], self.df["scaled_sugars"][i], self.df["scaled_fat"][i], self.df["scaled_saturated"][i], self.df["scaled_fiber"][i], self.df["scaled_proteins"][i], self.df["scaled_salt"][i], self.df["scaled_sodium"][i]]))
        self.inputs = np.asarray(self.inputs)
    # Split inputs and labels into training and test sets.
    def split_data(self):
        l = len(self.df)
        # (90%, 10%) - (training, test)
        self.train_inputs = self.inputs[0:int(l*0.9)]
        self.test_inputs = self.inputs[int(l*0.9):]
        self.train_labels = self.labels[0:int(l*0.9)]
        self.test_labels = self.labels[int(l*0.9):]
    # Build and train an artificial neural network (ANN) to make predictions on the Nutri-Score values (food health category) based on nutrient profiling.
    def build_and_train_model(self):
        # Build the neural network:
        self.model = keras.Sequential([
            keras.Input(shape=(9,)),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(512, activation='relu'),
            keras.layers.Dense(1024, activation='relu'),
            keras.layers.Dense(2048, activation='relu'),
            keras.layers.Dense(4, activation='softmax')
        ])
        # Compile:
        self.model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=['accuracy'])
        # Train:
        self.model.fit(self.train_inputs, self.train_labels, epochs=15)
        # Test the accuracy:
        print("\n\nModel Evaluation:")
        test_loss, test_acc = self.model.evaluate(self.test_inputs, self.test_labels) 
        print("Evaluated Accuracy: ", test_acc)
    # Save the model for further usage on Raspberry Pi:
    def save_model(self):
        self.model.save("E:\PYTHON\Barcode_Based_Nutrient_Profiling\ANN_Nutrient_Profiling.h5")
    # Convert the TensorFlow Keras H5 model (.h5) to a TensorFlow Lite model (.tflite) to run it on Raspberry Pi.
    def convert_TF_model(self, path):
        model = tf.keras.models.load_model(path + ".h5")
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        # Save the TensorFlow Lite model.
        with open(path + '.tflite', 'wb') as f:
            f.write(tflite_model)
        print("\r\nTensorFlow Keras H5 model converted to a TensorFlow Lite model...\r\n")
    # Run Artificial Neural Network (ANN):
    def Neural_Network(self, save):
        self.define_and_assign_labels()
        self.scale_data_and_define_inputs()
        self.split_data()
        self.build_and_train_model()
        if save:
            self.save_model()
            
# Read the generated data set of food products:
csv_path = "E:\PYTHON\Barcode_Based_Nutrient_Profiling\product_database.csv"
df = pd.read_csv(csv_path)

# Define a new class object named 'food_products':
food_products = Nutrient_Profiling(df)

# Visualize data:
#food_products.data_visualization()

# Artificial Neural Network (ANN):
food_products.Neural_Network(True)

# Convert the TensorFlow Keras H5 model to a TensorFlow Lite model:
#food_products.convert_TF_model("E:\PYTHON\Barcode_Based_Nutrient_Profiling\ANN_Nutrient_Profiling")
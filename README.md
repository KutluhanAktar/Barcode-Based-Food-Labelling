# Barcode-Based-Food-Labelling
Collect nutrition facts by barcodes to distinguish healthy and unhealthy foods w/ a neural network model predicting Nutri-Score classes.

Even though some countries apply strict regulations on describing ingredients of foods and systematic methods for categorizing foods according to their nutritional quality (nutrient profiling), yet it is not enough to determine healthy and unhealthy foods worldwide. Because in most countries, food packagings only present a list of ingredients and a calorie chart for purchasers to interpret whether it is a portion of healthy or unhealthy food. And, merely printing a list of information on packaging without any indications of health stats is not a suitable way to categorize foods:

First of all, in that regard, it requires us to have some preliminary information about food ingredients to interpret their health stats.

For some of us, it can be struggling to inspect packaging information on ingredients, for instance, elderly and children.

And, most of the time, food packaging includes limited and constricted nutritional facts for us to decide whether it is a portion of healthy food or not.

Aside from the dearth of support worldwide, there are several well-developed approaches for categorizing foods using nutrient profiling, which directly present the health stats of a food product. As discussed by WHO, it is crucial to develop a nutrient profiling model for categorizing foods while considering the current objectives of nutrition policies: "A discussion on nutrient-profiling methods at a WHO forum and technical meeting on marketing in 2006 recognized the contextual nature of the task, namely that nutrient-profiling systems should aim 'to categorize foods according to their nutritional composition while taking into account current objectives of nutrition policies'. The objective in most cases is to increase the proportion of the population adhering to national food-based dietary guidelines.[1]"

Furthermore, as shown in most studies, having a well-developed and easy-to-understand nutrient profiling system can change our overall perspective when purchasing foods at food stores, restaurants, etc. "The development of nutrient-profiling schemes is clearly beneficial in a wide range of applications, both commercial and health-related. For instance, the use of nutrient profiling to support the European health claims regulations is under consideration by the European Commission. Similar measures can be suggested for catering outlets, where a profiling scheme such as traffic light signaling could help customers select healthier items from menus in advance of ordering their food[1]."

After doing some research on several nutrient profiling methods, I decided to build an artificial neural network (ANN) model based on the classification model to interpret nutrition facts and nutrient levels of various food products to predict the healthiness level of a product even with meager information in simple and easy-to-understand classes (labels). Due to its advanced scientific algorithm, I decided to utilize an improved version of the Nutri-Score system for my neural network model. The Nutri-Score, also known as the 5-Colour Nutrition Label or 5-CNL, is a nutritional rating system selected by the French government in March 2017 to be displayed on food products after compared against several labels proposed by industry or retailers. It relies on a nutrient profiling system computation derived from the United Kingdom Food Standards Agency nutrient profiling system (FSA score). For my neural network model, I improved the original scientific algorithm of Nutri-Score by adding some extra parameters:

Calcium

Carbon Footprint (CO2)

Ecological Footprint (EF)

Before building and testing my neural network, I developed a web application in PHP to collate product characteristics (nutrition facts, nutrient levels, etc.) with product barcodes via the Open Food Facts JSON API. Since searching products with barcodes is the most effortless way possible to distinguish different products worldwide. Then, I created a data set of various handpicked products from the Open Food Facts database, presenting all the required information to train my neural network model.

After completing the data set, I built my artificial neural network (ANN) with TensorFlow to make predictions on the healthiness classes (labels) based on the Nutri-Score values. Theoretically, I assigned a healthiness class (label) for each product after applying my improved Nutri-Score algorithm to the data set:

Nutritious

Healthy

Less Healthy

Unhealthy

Then, after testing, I converted the TensorFlow Keras H5 model to a TensorFlow Lite model to execute it on Raspberry Pi. I decided to connect a barcode scanner to Raspberry Pi to elicit food product barcodes easily to run the neural network model with data transferred by the web application to predict products' healthiness classes (labels). In that regard, by merely scanning food product barcodes, Raspberry Pi makes predictions on the healthiness level of different foods without needing us to scrutinize packaging information.

So, this is my project in a nutshell 😃

You can inspect the project tutorial here:

https://www.hackster.io/kutluhan-aktar/barcode-based-nutrient-profiling-and-food-labelling-w-tf-28a371

<?php

# Define the barcode_scanner class and its functions.
class barcode_scanner{
	# Elicit and print information as to the given barcode - nutrient levels, nutrition facts, etc.
	public function print_product_info($barcode){
		# Make an HTTP Get request to the Open Food Facts JSON API to collate data on the product characteristics with the given barcode.
		$data = json_decode(file_get_contents("https://world.openfoodfacts.org/api/v0/product/".$barcode.".json", TRUE));
		# If the barcode found:
		if($data->status_verbose != "product not found"){
			# Create the query array with the incoming data:
			$query = array(
				"name" => is_null($data->product->brands) ? " " : $data->product->brands,
				"type" => is_null($data->product->product_name) ? " " : $data->product->product_name,
				"manufacturing_places" => (is_null($data->product->manufacturing_places) || $data->product->manufacturing_places == "") ? "Worldwide" : $data->product->manufacturing_places,
				"quantity" => is_null($data->product->product_quantity) ? 100 : (int)$data->product->product_quantity,
				"serving_quantity" => is_null($data->product->serving_quantity) ? 100 : (int)$data->product->serving_quantity,
				"energy-kcal_100g" => is_null($data->product->nutriments->{'energy-kcal_100g'}) ? 0 : $data->product->nutriments->{'energy-kcal_100g'},
				"energy-kcal_serving" => is_null($data->product->nutriments->{'energy-kcal_serving'}) ? $data->product->nutriments->{'energy-kcal_100g'} : $data->product->nutriments->{'energy-kcal_serving'},
				"carbohydrates_100g" => is_null($data->product->nutriments->carbohydrates_100g) ? 0 : $data->product->nutriments->carbohydrates_100g,
				"carbohydrates_serving" => is_null($data->product->nutriments->carbohydrates_serving) ? $data->product->nutriments->carbohydrates_100g : $data->product->nutriments->carbohydrates_serving,
				"sugars_100g" => is_null($data->product->nutriments->sugars_100g) ? 0 : $data->product->nutriments->sugars_100g,
				"sugars_serving" => is_null($data->product->nutriments->sugars_serving) ? $data->product->nutriments->sugars_100g : $data->product->nutriments->sugars_serving,
				"fat_100g" => is_null($data->product->nutriments->fat_100g) ? 0 : $data->product->nutriments->fat_100g,
				"fat_serving" => is_null($data->product->nutriments->fat_serving) ? $data->product->nutriments->fat_100g : $data->product->nutriments->fat_serving,
				"saturated-fat_100g" => is_null($data->product->nutriments->{'saturated-fat_100g'}) ? 0 : $data->product->nutriments->{'saturated-fat_100g'},
				"saturated-fat_serving" => is_null($data->product->nutriments->{'saturated-fat_serving'}) ? $data->product->nutriments->{'saturated-fat_100g'} : $data->product->nutriments->{'saturated-fat_serving'},		
				"fruits_vegetables_100g" => is_null($data->product->nutriments->{'fruits-vegetables-nuts-estimate-from-ingredients_100g'}) ? 0 : $data->product->nutriments->{'fruits-vegetables-nuts-estimate-from-ingredients_100g'},
				"fiber_100g" => (is_null($data->product->nutriments->fiber_100g) || $data->product->nutriments->fiber_100g == "") ? 0 : $data->product->nutriments->fiber_100g,
				"fiber_serving" => (is_null($data->product->nutriments->fiber_serving) || $data->product->nutriments->fiber_serving == "") ? 0 : $data->product->nutriments->fiber_serving,
				"proteins_100g" => is_null($data->product->nutriments->proteins_100g) ? 0 : $data->product->nutriments->proteins_100g,
				"proteins_serving" => is_null($data->product->nutriments->proteins_serving) ? $data->product->nutriments->proteins_100g : $data->product->nutriments->proteins_serving,		
				"salt_100g" => is_null($data->product->nutriments->salt_100g) ? 0 : $data->product->nutriments->salt_100g,
				"salt_serving" => is_null($data->product->nutriments->salt_serving) ? $data->product->nutriments->salt_100g : $data->product->nutriments->salt_serving,
				"sodium_100g" => is_null($data->product->nutriments->sodium_100g) ? 0 : $data->product->nutriments->sodium_100g,
				"sodium_serving" => is_null($data->product->nutriments->sodium_serving) ? $data->product->nutriments->sodium_100g : $data->product->nutriments->sodium_serving,
				"calcium_100g" => (is_null($data->product->nutriments->calcium_100g) || $data->product->nutriments->calcium_100g == "") ? 0 : $data->product->nutriments->calcium_100g,
				"calcium_serving" => is_null($data->product->nutriments->calcium_serving) ? 0 : $data->product->nutriments->calcium_serving,			
				"nutri_score" => is_null($data->product->nutriscore_data->score) ? 0 : $data->product->nutriscore_data->score,
				"nutri_grade" => is_null($data->product->nutriscore_data->grade) ? "Undefined" : $data->product->nutriscore_data->grade,
				"co2_total" => is_null($data->product->ecoscore_data->agribalyse->co2_total) ? 1 : $data->product->ecoscore_data->agribalyse->co2_total,
				"ef_total" => is_null($data->product->ecoscore_data->agribalyse->ef_total) ? 0.25 : $data->product->ecoscore_data->agribalyse->ef_total
			);
			// Print the recent query in JSON with the requested values:
			echo(json_encode($query));
		}	
	}
}

# Define the new 'product' class object.
error_reporting(0);
$product = new barcode_scanner();
# Get the product information of the given barcode:
if(isset($_GET["barcode"]) && $_GET["barcode"] != ""){
	$product->print_product_info($_GET["barcode"]);
}
?>
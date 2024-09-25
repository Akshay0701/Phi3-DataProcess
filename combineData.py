import os
import json
import shutil

# Define the path to the main directory containing all PDF folders
main_directory = "outputs"

# Path where the main combined JSON and images will be stored
output_directory = "combined_datacopy"
output_images_directory = os.path.join(output_directory, "images")
output_json_file = os.path.join(output_directory, "combined_data.json")

# Create output directories if they don't exist
os.makedirs(output_directory, exist_ok=True)
os.makedirs(output_images_directory, exist_ok=True)

# Initialize the combined list for JSON output
combined_data = []

# Function to process each folder and combine data
def process_folder(folder_name, folder_path, image_counter):
    # Path to the normalized figure-caption JSON file
    json_file_path = os.path.join(folder_path, "normalized_figure_caption_data.json")
    
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        print(f"No JSON file found in {folder_path}")
        return image_counter
    
    # Load the JSON data
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        folder_data = json.load(json_file)

    # Process each figure and caption in the folder
    for figure, caption in folder_data.items():
        # Generate a unique image file name using the image counter
        unique_image_name = f"{image_counter:012}.png"  # Image name with leading zeros
        image_id = f"{image_counter:012}"  # ID with leading zeros (12 digits)
        
        # Find the corresponding image file in the folder (assuming image names follow a pattern)
        found_image = False
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".png") and not file_name.startswith("0_image_"):  # Ignore the irrelevant first page images
                original_image_path = os.path.join(folder_path, file_name)
                new_image_path = os.path.join(output_images_directory, unique_image_name)
                
                # Copy the image to the output images folder with the unique name
                shutil.copy(original_image_path, new_image_path)
                print(f"Copied {original_image_path} to {new_image_path}")
                
                # Add the figure and image reference to the combined data
                combined_data.append({
                    "id": image_id,
                    "image": unique_image_name,
                    "captions": caption
                })
                
                found_image = True
                image_counter += 1  # Increment the image counter globally
                break  # Exit the loop after copying the first relevant image

        if not found_image:
            print(f"No relevant image found for figure {figure} in {folder_path}")

    return image_counter

# Start processing each folder and combining data
image_counter = 1  # Start image numbering from 1 globally
for folder_name in os.listdir(main_directory):
    folder_path = os.path.join(main_directory, folder_name)
    
    # Only process directories
    if os.path.isdir(folder_path):
        print(f"Processing folder: {folder_name}")
        image_counter = process_folder(folder_name, folder_path, image_counter)

# Save the combined JSON data to the output file
with open(output_json_file, "w", encoding="utf-8") as output_json:
    json.dump(combined_data, output_json, indent=4)

print(f"Combined JSON data saved to {output_json_file}")
print(f"All images saved in {output_images_directory}")

import os

# Define the path to the main directory containing all PDF folders
main_directory = "outputs"

# Function to remove first page images from a single folder
def remove_first_page_images(folder_path):
    # List all files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file matches the pattern '0_image_x.png'
        if file_name.startswith("0_image_") and file_name.endswith(".png"):
            file_path = os.path.join(folder_path, file_name)
            # Remove the image file
            try:
                os.remove(file_path)
                print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

# Iterate over all folders in the main directory
for folder_name in os.listdir(main_directory):
    folder_path = os.path.join(main_directory, folder_name)
    
    # Only process directories (each directory represents one PDF)
    if os.path.isdir(folder_path):
        print(f"Processing folder: {folder_name}")
        remove_first_page_images(folder_path)

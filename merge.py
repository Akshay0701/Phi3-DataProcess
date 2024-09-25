import os
import re
import json

# Define the path to the main directory containing all PDF folders
main_directory = "outputs"

# Function to process a single folder
def process_folder(folder_path):
    # Find the markdown file in the folder (assuming there's only one .md file)
    md_file = None
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".md"):
            md_file = os.path.join(folder_path, file_name)
            break
    
    if not md_file:
        print(f"No markdown file found in {folder_path}")
        return

    # Read the markdown file
    with open(md_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Regex pattern to capture figure references
    figure_pattern = r'(?:[Ff]ig(?:ure)?\.?\s*\d+)'

    # Dictionary to store normalized figure-caption pairs
    figure_caption_dict = {}

    # Find all figure references and extract the associated paragraphs
    matches = re.finditer(figure_pattern, content)

    for match in matches:
        # Find the figure reference (e.g., Fig. 1 or Figure 1)
        figure_ref = match.group(0)

        # Normalize figure references (convert all to "Figure X" format)
        normalized_figure = re.sub(r'[Ff]ig(?:ure)?\.?\s+', 'Figure ', figure_ref).strip()

        # Get the paragraph around the figure reference
        start = content.rfind('\n', 0, match.start())
        end = content.find('\n', match.end())

        if start == -1: start = 0  # Handle case where figure is at the beginning
        if end == -1: end = len(content)  # Handle case where figure is at the end

        paragraph = content[start:end].strip()

        # Add the normalized figure and its paragraph to the dictionary
        if normalized_figure not in figure_caption_dict:
            figure_caption_dict[normalized_figure] = paragraph
        else:
            # Combine captions if multiple entries for the same figure
            figure_caption_dict[normalized_figure] += ' ' + paragraph

    # Save the result into a JSON file
    output_file = os.path.join(folder_path, "normalized_figure_caption_data.json")
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(figure_caption_dict, json_file, indent=4)

    print(f"Figure-caption data saved to {output_file}")

# Iterate over all folders in the main directory
for folder_name in os.listdir(main_directory):
    folder_path = os.path.join(main_directory, folder_name)
    
    # Only process directories (each directory represents one PDF)
    if os.path.isdir(folder_path):
        print(f"Processing folder: {folder_name}")
        process_folder(folder_path)

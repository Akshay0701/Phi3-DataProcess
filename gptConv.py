import json
import random
import openai
import os
from time import sleep

# Set your OpenAI API key
openai.api_key = "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"

def generate_questions(caption):
    questions = [
        "What type of chart/graph is this?",
        "What are the axes labels and units?",
        "What is the trend shown in the data?",
        "What are the key data points or outliers?",
        "What conclusions can be drawn from the data?",
        "What is the range of the data?",
        "What is the distribution of the data?",
        "Are there any error bars or uncertainties displayed?",
        "What is the scale of the graph?",
        "Is there a trend line, regression line, or curve fitting?",
        "What is the purpose of the figure?",
        "What are the labels and annotations in the figure?",
        "What technique or method is shown in the image?",
        "What are the key components or regions in the figure?",
        "What is the scale or magnification?",
        "What are the steps in the process illustrated?",
        "What conclusions or observations are made based on this figure?",
        "Is the figure a representation of experimental data or a conceptual model?",
        "What type of microscopy technique was used?",
        "What magnification level is being used?",
        "What are the different materials or features visible in the image?",
        "What is the resolution of the image?",
        "What are the key features or patterns in the image?",
        "What variables are represented in the table?",
        "What are the key values or data points?",
        "What comparisons can be made between different entries in the table?",
        "Are there any missing or incomplete data points?",
        "What method was used to generate this image?",
        "What is the temperature, pressure, or experimental condition depicted?",
        "What do the colors or shading represent in the image?",
        "What are the key findings or observations?"
    ]
    
    return random.sample(questions, random.randint(5, 6))

def generate_answer(question, caption):
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant analyzing scientific images and data."},
                    {"role": "user", "content": f"Given this image caption: '{caption}'\n\nAnswer this question: {question}"}
                ],
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
            )
            
            return response.choices[0].message['content'].strip()
        
        except openai.error.RateLimitError:
            if attempt < max_retries - 1:
                print(f"Rate limit reached. Retrying in {retry_delay} seconds...")
                sleep(retry_delay)
            else:
                print("Max retries reached. Returning placeholder answer.")
                return f"Based on the caption, the answer to '{question}' is: [Unable to generate answer due to rate limiting]"
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"Based on the caption, the answer to '{question}' is: [Unable to generate answer due to an error]"

def process_data(input_data):
    output_data = []
    
    for item in input_data:
        conversations = []
        questions = generate_questions(item['captions'])
        
        conversations.append({
            "from": "human",
            "value": f"<image>\n{questions[0]}"
        })
        conversations.append({
            "from": "gpt",
            "value": generate_answer(questions[0], item['captions'])
        })
        
        for question in questions[1:]:
            conversations.append({
                "from": "human",
                "value": question
            })
            conversations.append({
                "from": "gpt",
                "value": generate_answer(question, item['captions'])
            })
        
        output_item = {
            "id": item['id'],
            "image": item['image'],
            "conversations": conversations
        }
        
        output_data.append(output_item)
    
    return output_data

# Load input data
with open('data.json', 'r') as f:
    input_data = json.load(f)

# Process data
output_data = process_data(input_data)

# Save output data
with open('output.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("Processing complete. Output saved to 'output.json'.")
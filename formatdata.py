import requests
from datasets import Dataset
import json
import time
import csv
import openai

# Set your OpenAI API key
openai.api_key = 

# Define the prompt template
meal_prompt_template = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}
"""
def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the model to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"An error occurred: {e}"

file_path = r'C:\Users\archi\OneDrive\Documents\GitHub\Cook-Buddy\RecipeNLG_dataset.csv'

examples = []

with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for i, row in enumerate(reader, start=1):
        name = row[1] 
        ingrd = row[2]
        instruct = row[3]
        
        instruction = "" #Do we add?
        input_context = f"Meal: {name}"
        output_response = f"Ingredients: {ingrd}, Instructions: {instruct}"
        prompt = "Given the recipe here, tell me what type of food is being cooked for example, Mexican, Asian or American, and also give me a predicted time that will take to cook the recipe. Respond in the format: Type of Food, Time. With one word for type of food and 2 for time" +  name + instruct 
        response = chat_with_gpt(prompt).split(",", 1)

        output_response = f"Cuisine: {response[0]}, Approximate Time: {response[1]}, Ingredients: {ingrd}, Instructions: {instruct}"
        input_context = f"Meal: {name}, Ingredients:{ingrd}, Cuisine Type: {response[0]} Approximate Time: {response[1]}"
        # Format with prompt template and add EOS token
        text = meal_prompt_template.format(instruction, input_context, output_response) + "<|endoftext|>"  # EOS token
        examples.append({"instruction": instruction, "input": input_context, "output": output_response, "text": text})
        if i > 15:
            break


# Convert to Hugging Face Dataset format
dataset = Dataset.from_list(examples)

# Print sample data for verification
print(dataset[0])

dataset.save_to_disk("./15datasettest")












# # Define a function to fetch data from TheMealDB API
# def fetch_meal_data(num_meals=10000):
#     meals = []
#     for _ in range(num_meals):
#         # Fetch a single random meal
#         response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
#         if response.status_code == 200:
#             data = response.json()
#             if data["meals"] is not None:
#                 meals.append(data["meals"][0])  # Append only the first meal object
#         time.sleep(0.1)  # Sleep to avoid hitting the server too quickly (politeness delay)

#     return meals

# # Define a function to format the data
# def format_meal_data_for_prompt(meals):
#     examples = []
#     for meal in meals:
#         instruction = "Describe the recipe and ingredients for the meal."
#         input_context = f"Meal: {meal['strMeal']}"
#         output_response = f"Ingredients: {meal['strIngredient1']}, {meal['strIngredient2']}, ...\nInstructions: {meal['strInstructions']}"

#         # Format with prompt template and add EOS token
#         text = meal_prompt_template.format(instruction, input_context, output_response) + "<|endoftext|>"  # EOS token
#         examples.append({"instruction": instruction, "input": input_context, "output": output_response, "text": text})
#     return examples

# # Fetch and format the data
# meals = fetch_meal_data()
# formatted_data = format_meal_data_for_prompt(meals)

# # Convert to Hugging Face Dataset format
# dataset = Dataset.from_list(formatted_data)

# # Print sample data for verification
# print(dataset[0])

# dataset.save_to_disk("./mydataset10k")



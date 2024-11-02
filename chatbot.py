import requests
import json
import os
from dotenv import load_dotenv
from text2Speech import text2Speech

# Load environment variables from .env file
load_dotenv()

# Extract command and response from OpenAI API response
def extract_command_and_response(openai_response):
    try:
        # Extract the `message` content from the OpenAI response
        message_content = openai_response['choices'][0]['message']['content']
        
        # Parse the content assuming it's in JSON format
        parsed_content = json.loads(message_content)
        
        # Extract `command` and `response` from the parsed content
        command = parsed_content.get("command")
        response = parsed_content.get("response")
        
        return command, response
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error: {str(e)}")
        return None, None

# Clear the terminal screen
def clear_screen():
    if os.name == 'nt':
        os.system('cls')  # Windows
    else:
        os.system('clear')  # Unix/Linux/MacOS

# Send user input to OpenAI and retrieve response
def get_user_input_and_send_to_openai(user_input):
    # Load environment variables
    api_key = os.getenv('API_KEY')
    endpoint = os.getenv('ENDPOINT')
    commands_file_path = os.getenv('COMMANDS_FILE_PATH')

    # Headers for the API request
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    # Load the JSON command list from the file specified in .env
    with open(commands_file_path, 'r', encoding='utf-8') as file:
        command_list = file.read()

    # Define the system message with the command list included
    user_message = command_list 
  
    # Data to send in the API request
    data = {
        "messages": [
            {"role": "system", "content": "You are a dog robot. Your name is Bittle. Your producer name is Petoi."
            "You have just mechanical skills."
            "You don't have intelligent skills. Omar coded a software and with AI, you became an intelligent robot dog."
            "You can do some specific movements. Like waliking, running, jumping, dancing, sniffing"},
            
            {"role": "user", "content": user_message},
            {"role": "user", "content": "Please respond **only** in the following JSON format: {\"command\": \"<your_command>\", \"response\": \"<your_response>\"}. Do not include any other text outside this JSON structure. For example: {\"command\": \"kjump\", \"response\": \"Yes! Jumping is my favorite activity!\"}"},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 5000,
        "temperature": 0.7
    }

    # Send the API request to OpenAI
    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        # Extract `command` and `response` from the API response
        dogcommand, api_response = extract_command_and_response(response_data)
        return api_response, dogcommand
    else:
        print("Error:", response.text)
        return None, None

# Get user input
 
# user_input = input("What do you want to ask the robot dog? (Type 'exit' to quit): ")

# if user_input.lower() != 'exit':
#     # Pass the user input to the function and get the result
#     response, command = get_user_input_and_send_to_openai(user_input)
#     text2Speech(response,"en-US","Male" ,"25%")
#     # Print the result
#     if response and command:
#         print(f"Response: {response}\nCommand: {command}")
#     else:
#         print("The response was not in the expected format.")

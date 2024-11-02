import os
import requests
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from chatbot import get_user_input_and_send_to_openai
from text2Speech import text2Speech
from DirectSerial import *
import os
import json

# Function to search for a specific command in a JSON file
def search_command_in_json(file_path, command_to_search):
    # Open and read the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # List to store the search results
    matches = []

    # Iterate through all commands in the data
    for entry in json_data.get("Shhet1", []):
        # If the "Command" field matches the "command_to_search", add the result to the list
        if entry.get("Command") == command_to_search:
            matches.append(entry)

    # Return matching results
    return matches


def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Mac and Linux (posix systems)
    else:
        os.system('clear')

# Example usage
clear_screen()
time.sleep(1)

# Load environment variables from the .env file
load_dotenv()

# Function to convert speech to text using Azure Speech Service
def speech_to_text(language="en-US"):
    # Retrieve the speech key and region from environment variables
    speech_key = os.getenv('SPEECH_KEY')
    region = os.getenv('REGION')
    
    if not speech_key or not region:
        raise ValueError("Speech key or region is not set in the environment variables.")
    
    # Configure Azure Speech
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    
    # Set up the speech recognizer with the specified language
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=language)
    
    print(f"Speak into your microphone (Language: {language}).")
    
    # Listen to the user and convert speech to text
    result = speech_recognizer.recognize_once()
    
    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
    
    return None


# Function to extract specific fields from the JSON response
def extract_field_from_json(response_json, field_name):
    try:
        keys = field_name.split(".")
        data = response_json
        for key in keys:
            # If 'key' is a number, treat it as a list index
            if key.isdigit():
                data = data[int(key)]
            else:
                data = data[key]
        return data
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error: {e} - Could not find or access '{field_name}' in the JSON response.")
        return None


# Function to send a chat request to Azure OpenAI
def send_chat_request(user_message):
    # Get API key and endpoint from environment variables
    api_key = os.getenv('API_KEY')
    endpoint = os.getenv('ENDPOINT')
    
    if not api_key or not endpoint:
        raise ValueError("API key or endpoint is not set in the environment variables.")
    
    # Set request headers
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    # Create the payload with the user message
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    # Send the request to Azure OpenAI
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()  # Raises an error for unsuccessful requests
        return response.json()  # Return the response in JSON format
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

# Main function for interaction
if __name__ == "__main__":
    while True:
      
        # You can use speech-to-text here or just text input for testing
        user_message = speech_to_text(language="en-US")
        # user_message = input("Type your message: ")  # Use input for testing purposes
        
        if user_message:
            # Send the text message to Azure OpenAI
            response, command = get_user_input_and_send_to_openai(user_message)
            print(response, command)  # Print the chatbot's response
            if response:
                text2Speech(response, language="en-US", gender="Male", rate="25%")
            if command:
                file_path = r'd:\petoi\commands.json' 
                results = search_command_in_json(file_path, command)
                if results:
                    changeLed1(1)
                    time.sleep(1)
                    send_dogcommand1(command, 4)
                    changeLed1(0)
                    send_dogcommand1("ksit", 1)

        else:
            print("No valid input was recognized.")

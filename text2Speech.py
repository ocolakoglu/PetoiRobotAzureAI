import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up your Azure Speech Service key and region
speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

def text2Speech(text, language="en-US", gender="Female", rate="0%"):
    # Check if speech_key and speech_region are loaded properly
    if not speech_key or not speech_region:
        raise ValueError("Azure Speech key or region is missing. Please check your .env file or environment variables.")
    
    # Initialize the Speech Config using your Azure Speech key and region
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    
    # Determine the voice based on the language and gender provided
    if language == "en-US":
        voice = "en-US-AriaNeural" if gender.lower() == "female" else "en-US-GuyNeural"
    elif language == "en-GB":
        voice = "en-GB-LibbyNeural" if gender.lower() == "female" else "en-GB-RyanNeural"
    elif language == "de-DE":
        voice = "de-DE-KatjaNeural" if gender.lower() == "female" else "de-DE-ConradNeural"
    else:
        # Default to US English if the language is not supported
        voice = "en-US-AriaNeural"

    # Set the voice in the speech configuration
    speech_config.speech_synthesis_voice_name = voice

    # Create the SSML structure to include the rate change
    ssml_string = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{language}'>
        <voice name='{voice}'>
            <prosody rate='{rate}'>
                {text}
            </prosody>
        </voice>
    </speak>
    """

    # Initialize the speech synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesize the text using SSML
    result = synthesizer.speak_ssml_async(ssml_string).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized successfully.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

# Example usage
# if __name__ == "__main__":
#     sample_text = "Hello, how can I assist you today?"
#     text2Speech(sample_text, language="en-US", gender="Male", rate="25%")  # Increase speed by 50%

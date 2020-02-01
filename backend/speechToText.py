from flask import Flask
app = Flask(__name__)
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech

@app.route('/speechToText')
def speechToText(uri):
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    audio = speech.types.RecognitionAudio(uri)
    
    config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code='en-US',
            sample_rate_hertz=44100)

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    return response.results.alternatives[0].transcript

if __name__ == '__main__':
    app.run()
from flask import Flask
app = Flask(__name__)
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


@app.route('/speechToText')
def speechToText():
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    audio = speech.types.RecognitionAudio(
    uri='gs://my-bucket/recording.flac')
    
    config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code='en-US',
            sample_rate_hertz=44100)

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

if __name__ == '__main__':
    app.run()
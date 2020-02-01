import io
import os
from google.cloud import speech

def speechToText(content):
    client = speech.SpeechClient()
    audio = {"content": content}
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US')
    response = client.recognize(config, audio)
    res = ""
    for result in response.results:
        # First alternative is the most probable result
        res += result.alternatives[0].transcript
        # print(type(result))
        # alternative = result.alternatives[0]
        # print(u"Transcript: {}".format(alternative.transcript)) 
    return res
from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import speechToText
import sentiment
from Microphone import *


app = Flask(__name__, static_folder="../frontend/build/static")
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
CORS(app)
nlu = sentiment.setup()


@app.route("/")
def root():
    return send_from_directory("../frontend/build", 'index.html')


@app.route("/getSentimentData", methods=['POST'])
def get_sentiment_data():
    data = request.get_data(cache=False)
    res = speechToText.speechToText(data)
    fin_res = sentiment.analyze(nlu, res)
    return fin_res["emotion"]["document"]["emotion"]


@app.route("/getSentimentDataStream", methods=["POST"])
def get_sentiment_data_stream():
    amt = int(request.args.get('split'))
    data = request.get_data(cache=False)
    res = speechToText.speechToText(data)[0:50]
    res = res.split()
    splits = [" ".join(res[0:i]) for i in range(len(res)//amt, len(res)+len(res)//amt, len(res)//amt)]
    print(splits)
    for i in range(len(splits)):
        splits[i] = sentiment.analyze(nlu, splits[i])["emotion"]["document"]["emotion"]
    return {"items": splits}


@socketio.on("getMicrophoneStream")
def get_mic_stream():
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", use_reloader=True, port=os.environ["PORT"] if "PORT" in os.environ else 5000, threaded=True)    
    socketio.run(app)
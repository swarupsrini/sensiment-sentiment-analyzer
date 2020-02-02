from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os
import speechToText
import sentiment
from Microphone import *


app = Flask(__name__, static_folder="../frontend/build/static")
app.secret_key = os.urandom(24)
CORS(app)
nlu = sentiment.setup()

language_code = 'en-US'  # a BCP-47 language tag

cache = {}

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
    # amt = int(request.args.get('split'))
    amt = 4
    name = int(request.args.get('split'))
    data = request.get_data(cache=False)
    res = speechToText.speechToText(data)[0:50]
    res = res.split()
    splits = [" ".join(res[0:i]) for i in range(len(res)//amt, len(res)+len(res)//amt, len(res)//amt)]
    print(splits)
    for i in range(len(splits)):
        splits[i] = sentiment.analyze(nlu, splits[i])[
            "emotion"]["document"]["emotion"]
    cache[name] = splits
    return {"items": splits}

@app.route("/getSentimentCache", methods=["POST"])
def get_cache():
    return cache

if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=True,
            port=os.environ["PORT"] if "PORT" in os.environ else 5000, threaded=True)

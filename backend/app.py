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
    amt = 3
    name = request.args.get('name')
    data = request.get_data(cache=False)
    ress = speechToText.speechToText(data)[0:50]
    res = ress.split()
    splits = [" ".join(res[0:i]) for i in range(len(res)//amt, len(res)+len(res)//amt, len(res)//amt)]
    data = sentiment.analyze(nlu, ress)
    keys = [data["keywords"][i]["text"] for i in range(len(data["keywords"]))]
    for i in range(len(splits)):
        splits[i] = sentiment.analyze(nlu, splits[i])["emotion"]["document"]["emotion"]
    ret = {}
    ret["anger"] = [splits[i]["anger"] for i in range(len(splits))]
    ret["sadness"] = [splits[i]["sadness"] for i in range(len(splits))]
    ret["joy"] = [splits[i]["joy"] for i in range(len(splits))]
    ret["fear"] = [splits[i]["fear"] for i in range(len(splits))]
    ret["disgust"] = [splits[i]["disgust"] for i in range(len(splits))]
    cache[name] = {"items": ret, "keywords": keys, "name": name}
    print({"items": ret, "keywords": keys, "name": name})
    return {"items": ret, "keywords": keys, "name": name}


@app.route("/getSentimentCache", methods=["POST"])
def get_cache():
    print(cache)
    return cache

if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=True,
            port=os.environ["PORT"] if "PORT" in os.environ else 5000, threaded=True)

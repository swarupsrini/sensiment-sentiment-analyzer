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
    ress = speechToText.speechToText(data)
    res = ress.split()
    splits = [" ".join(res[0:i]) for i in range(len(res)//amt, len(res)+len(res)//amt, len(res)//amt)]
    data = sentiment.analyze(nlu, ress)
    keys = [data["keywords"][i]["text"] for i in range(len(data["keywords"]))]
    for i in range(len(splits)):
        splits[i] = sentiment.analyze(nlu, splits[i])["emotion"]["document"]["emotion"]

    items = []
    items.append({"id": "anger",
                  "data": [{"x": i, "y": splits[i]["anger"]} for i in range(len(splits))]
                })
    items.append({"id": "sadness",
                  "data": [{"x": i, "y": splits[i]["sadness"]} for i in range(len(splits))]
                })
    items.append({"id": "joy",
                  "data": [{"x": i, "y": splits[i]["joy"]} for i in range(len(splits))]
                })
    items.append({"id": "fear",
                  "data": [{"x": i, "y": splits[i]["fear"]} for i in range(len(splits))]
                })
    items.append({"id": "disgust",
                  "data": [{"x": i, "y": splits[i]["disgust"]} for i in range(len(splits))]
                })
    ret = {"items": items, "keywords": keys, "name": name, "text": ress}
    cache[name] = ret
    return ret


@app.route("/getSentimentCache", methods=["POST"])
def get_cache():
    print(cache)
    return cache

if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=True,
            port=os.environ["PORT"] if "PORT" in os.environ else 5000, threaded=True)

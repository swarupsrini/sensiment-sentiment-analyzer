from flask import Flask, request, send_from_directory
from flask_cors import CORS
import speechToText
import sentiment

app = Flask(__name__, static_folder="../frontend/build/static")
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
    

if __name__ == "__main__":
    app.run(use_reloader=True, port=5000, threaded=True)

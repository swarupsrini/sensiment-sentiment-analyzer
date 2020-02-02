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
    response = speechToText.speechToText(data)
    res = ""
    for result in response.results:
        res += result.alternatives[0].transcript
    fin_res = sentiment.analyze(nlu, res)
    return fin_res["emotion"]["document"]["emotion"]


@app.route("/getSentimentDataStream", methods=["POST"])
def get_sentiment_data_stream():
    amt = request.args.get('split')
    data = request.get_data(cache=False)
    res = speechToText.speechToText(data)


if __name__ == "__main__":
    app.run(use_reloader=True, port=5000, threaded=True)

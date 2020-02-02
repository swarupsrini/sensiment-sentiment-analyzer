from flask import Flask, request, jsonify
from google.cloud import storage
from flask_cors import CORS
import speechToText
import sentiment

app = Flask(__name__)
CORS(app)


@app.route("/getSentimentData", methods=['POST'])
def get_sentiment_data():
    data = request.get_data(cache=False)
    res = speechToText.speechToText(data)
    # print(res)
    finRes = sentiment.analyze(sentiment.setup(), res)
    print(finRes)
    

if __name__ == "__main__":
    app.run()

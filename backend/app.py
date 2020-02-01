from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

@app.route("/getSentimentData", methods=['POST'])
def get_sentiment_data():
    # save file
    data = request.get_data(cache=False)
    print(data)
    with open("song.mp3", "wb") as song:
        song.write(data)
    
    
from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

@app.route("/getSentimentData", methods=['POST'])
def get_sentiment_data():
    pass
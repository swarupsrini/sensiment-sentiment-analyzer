from flask import Flask, request, jsonify
from google.cloud import storage
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/getSentimentData", methods=['POST'])
def get_sentiment_data():
    # save file
    data = request.get_data(cache=False)
    print(request.get_data())
    print(data)
    with open("song.mp3", "wb") as song:
        song.write(data)

    # upload to blob
    bucket_name = "recording-for-speech"
    source_file_name = "song.mp3"
    destination_blob_name = "song.mp3"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    #


if __name__ == "__main__":
    app.run()

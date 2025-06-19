from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend access

@app.route('/videos', methods=['GET'])
def get_videos():
    video_urls = [
        "https://www.w3schools.com/html/mov_bbb.mp4",
        "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"
    ]
    return jsonify(video_urls)

if __name__ == '__main__':
    app.run(debug=True)

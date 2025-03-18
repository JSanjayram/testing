from flask import Flask, request, jsonify
from pytubefix import YouTube

app = Flask(__name__)

@app.route('/get_audio_stream', methods=['POST'])
def get_audio_stream():
    try:
        # Parse request JSON to get YouTube URL
        data = request.get_json()
        youtube_url = data.get("url")
        if not youtube_url:
            return jsonify({"error": "URL is required"}), 400

        # Use pytubefix to extract audio stream URL
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            return jsonify({"error": "No audio stream found"}), 404

        # Return the audio stream URL
        return jsonify({"audio_stream_url": audio_stream.url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

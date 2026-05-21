import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from yt_dlp import YoutubeDL

app = Flask(__name__)
CORS(app)  # Allows your mobile HTML file to talk to this API safely

@app.route('/api/convert', methods=['GET'])
def convert():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "msg": "Missing 'url' parameter"}), 400

    # Configure yt-dlp to just extract information without downloading the full video
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Extract the title and the direct, high-speed audio stream link
            title = info.get('title', 'Audio Track')
            audio_url = info.get('url')
            
            return jsonify({
                "status": "ok",
                "title": title,
                "link": audio_url  # Direct stream URL that acts as a download link
            })
            
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == '__main__':
    # Use environment port for cloud deployment compatibility
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

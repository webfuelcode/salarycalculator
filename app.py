from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/info")
def get_info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    ydl_opts = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = []
    for f in info['formats']:
        if f.get('ext') == 'mp4' and f.get('height'):
            formats.append({
                "format_id": f['format_id'],
                "resolution": f"{f.get('height')}p",
                "filesize": round((f.get('filesize') or 0) / 1024 / 1024, 2),
                "url": f['url']
            })

    audios = []
    for f in info['formats']:
        if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
            audios.append({
                "abr": f.get('abr'),
                "ext": f.get('ext'),
                "filesize": round((f.get('filesize') or 0) / 1024 / 1024, 2),
                "url": f['url']
            })

    return jsonify({
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "video_formats": formats,
        "audio_formats": audios
    })

@app.route("/")
def home():
    return jsonify({"message": "yt-dlp API is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

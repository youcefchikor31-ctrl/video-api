from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # للسماح لموقعك على جيت هاب بالاتصال بالسيرفر

# هذا المسار مخصص لكي يظل السيرفر مستيقظاً
@app.route('/')
def home():
    return "Server is running! 🚀"

# هذا المسار مخصص لجلب الفيديو
@app.route('/get_video', methods=['GET'])
def get_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "يرجى إرسال الرابط"}), 400
    
    ydl_opts = {'format': 'best', 'quiet': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_url = info.get('url')
            return jsonify({"success": True, "download_link": direct_url})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

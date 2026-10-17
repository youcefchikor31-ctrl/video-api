from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Server is running! 🚀"

@app.route('/get_video', methods=['GET'])
def get_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "يرجى إرسال الرابط"}), 400
    
    try:
        # التحقق مما إذا كان الرابط لتيك توك
        if 'tiktok.com' in video_url:
            # استخدام API مجاني مخصص لتيك توك لتخطي الحماية (وبدون علامة مائية)
            tikwm_api = f"https://www.tikwm.com/api/?url={video_url}"
            response = requests.get(tikwm_api).json()
            
            if response.get('code') == 0:
                direct_url = response['data']['play'] 
                return jsonify({"success": True, "download_link": direct_url})
            else:
                return jsonify({"success": False, "error": "حماية تيك توك منعت الجلب أو الرابط خاطئ."}), 400
                
        else:
            # استخدام yt-dlp لباقي المواقع (انستغرام وغيرها)
            ydl_opts = {'format': 'best', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                direct_url = info.get('url')
                return jsonify({"success": True, "download_link": direct_url})
                
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

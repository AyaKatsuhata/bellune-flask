from flask import Flask, request, jsonify
from supabase import create_client, Client
import os
from generate_personal_image import generate_image_from_json  # ← 画像生成関数
from dotenv import load_dotenv
import logging
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = os.path.join(LOG_DIR, f'server_{datetime.now().strftime("%Y%m%d")}.log')
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

load_dotenv()

app = Flask(__name__)

# Supabaseのクライアント設定
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/generate_personal_image', methods=['POST'])
def generate_personal_image():
    try:
        logging.info("リクエストデータ: %s", request.get_data(as_text=True))
        data = request.get_json()
        print("受信データ:", data)

        # GPTのJSON出力
        user_json = {
            "personality": data["json"]["personality"],
            "values": data["json"]["values"],
            "mission": data["json"]["mission"],
            "love": data["json"]["love"],
            "talent": data["json"]["talent"],
            "message": data["json"]["message"],
            "challenge": data["json"]["challenge"],
            "pattern": data["json"]["pattern"]
        }

        # その他の情報
        name = data["name"]
        line_id = data["lineId"]

        # ① 画像生成
        image_path = generate_image_from_json(user_json, name, line_id)

        # ② Supabaseにアップロード
        with open(image_path, 'rb') as f:
            file_data = f.read()

        file_name = f"{line_id}_fortune.png"
        logging.info("画像生成完了: %s", file_name)
        supabase.storage.from_("personal-images").upload(file_name, file_data, {"content-type": "image/png"})

        # ③ 公開URLを生成
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/personal-images/{file_name}"
        logging.info("画像パス: %s", public_url)

        return jsonify({"imageUrl": public_url})

    except Exception as e:
        print("画像生成エラー:", e)
        logging.info("画像生成エラー: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
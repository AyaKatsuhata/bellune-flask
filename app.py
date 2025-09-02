# app.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def generate_image_from_text(text, name, birthdate, birthplace, birthtime, lineId):
    # ここに既存の画像生成処理を呼び出す
    output_path = f"/tmp/{lineId}_generated.png"
    # ダミーでファイルを作るだけ（仮の処理）
    with open(output_path, 'w') as f:
        f.write("dummy image content")
    return output_path

@app.route("/generate_personal_image", methods=["POST"])
def generate_personal_image():
    data = request.get_json()
    try:
        image_path = generate_image_from_text(
            data["text"],
            data["name"],
            data["birthdate"],
            data["birthplace"],
            data["birthtime"],
            data["lineId"]
        )
        image_url = f"https://pay.bellune.jp/generated-images/{os.path.basename(image_path)}"
        return jsonify({ "imageUrl": image_url })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
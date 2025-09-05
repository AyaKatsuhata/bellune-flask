from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 1080, 1920

positions = {
    "personality": (70, 170, 400, 600),
    "values": (605, 130, 420, 280),
    "mission": (605, 515, 420, 280),
    "love": (55, 970, 280, 450),
    "talent": (405, 970, 280, 450),
    "message": (760, 970, 280, 450),
    "challenge": (60, 1550, 420, 350),
    "pattern": (600, 1550, 420, 350),
}

def draw_multiline(draw, text, position, font, max_width, max_height):
    x, y = position
    line_height = font.size + 15
    current_line = ""
    lines = []
    for char in text:
        test_line = current_line + char
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = char
    if current_line:
        lines.append(current_line)

    for line in lines:
        if y + line_height - position[1] > max_height:
            break
        draw.text((x, y), line, font=font, fill="black")
        y += line_height

def generate_image_from_json(user_json, name, line_id):
    try:
        bg_path = "./public/template/background.png"
        output_path = f"/tmp/{line_id}_fortune.png"

        img = Image.open(bg_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # Ubuntu想定フォント（環境に応じて変更）
        # font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans CJK JP:style=Regular"
        font_path = "/System/Library/Fonts/Helvetica.ttc"
        font = ImageFont.truetype(font_path, 26)

        for key, (x, y, w, h) in positions.items():
            text = user_json.get(key, "")
            draw_multiline(draw, text, (x, y), font, max_width=w, max_height=h)

        img.save(output_path, format="PNG")
        return output_path

    except Exception as e:
        raise RuntimeError(f"画像生成に失敗しました: {e}")
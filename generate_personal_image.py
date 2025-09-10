from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 1080, 1920

positions = {
    "personality": (50, 140, 440, 600),
    "values": (590, 115, 440, 280),
    "mission": (590, 495, 440, 280),
    "love": (45, 930, 290, 460),
    "talent": (395, 930, 290, 460),
    "message": (750, 930, 290, 456),
    "challenge": (40, 1530, 460, 370),
    "pattern": (580, 1530, 460, 370),
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
        output_path = f"./tmp/{line_id}_fortune.png"

        img = Image.open(bg_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 本番フォント
        # font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
        # 開発フォント
        font_path = "/Library/Fonts/Arial Unicode.ttf"
        # font = ImageFont.truetype(font_path, 26)

        for key, (x, y, w, h) in positions.items():
            text = user_json.get(key, "")
            font = get_best_font_size(draw, text, font_path, w, h)
            draw_multiline(draw, text, (x, y), font, max_width=w, max_height=h)

        img.save(output_path, format="PNG")
        return output_path

    except Exception as e:
        raise RuntimeError(f"画像生成に失敗しました: {e}")

def get_best_font_size(draw, text, font_path, max_width, max_height, min_size=16, max_size=36):
    for size in range(max_size, min_size - 1, -1):
        font = ImageFont.truetype(font_path, size)
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

        total_height = line_height * len(lines)
        if total_height <= max_height:
            return font  # このサイズでOK
    return ImageFont.truetype(font_path, min_size)  # 最小サイズに fallback
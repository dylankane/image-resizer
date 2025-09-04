from PIL import Image
import subprocess
import os

PRESETS = {
    "logo": 200,
    "thumbnail": 400,
    "grid": 800,
    "main": 1200,
    "hero": 1600,
    "full": 1920
}

REFERENCE_SCREEN_WIDTH = 1440
SMALL_SCREEN_WIDTH = 768

source_file = "sources.txt"
output_file = "media.txt"

def get_image_dimensions(path):
    try:
        img = Image.open(path)
        return img.size
    except Exception as e:
        print(f"Error reading image: {path} ({e})")
        return None

def get_video_dimensions(path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            width, height = map(int, result.stdout.strip().split("x"))
            return (width, height)
    except Exception as e:
        print(f"Error reading video: {path} ({e})")
    return None

def interpret_width_input(user_input):
    tokens = user_input.strip().lower().split()
    if not tokens:
        return None

    width_part = tokens[0]
    base = REFERENCE_SCREEN_WIDTH

    if len(tokens) > 1 and tokens[1] == "small":
        base = SMALL_SCREEN_WIDTH

    if width_part.endswith("px"):
        return int(width_part[:-2])
    elif width_part.endswith("%"):
        pct = int(width_part[:-1])
        return int((pct / 100.0) * base)
    elif width_part in PRESETS:
        return PRESETS[width_part]
    else:
        try:
            return int(width_part)
        except:
            return None

def process_file(path):
    if not os.path.isfile(path):
        print(f"❌ File not found: {path}")
        return None

    ext = os.path.splitext(path)[1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        dims = get_image_dimensions(path)
    elif ext in [".mp4", ".mov", ".avi", ".webm", ".mkv"]:
        dims = get_video_dimensions(path)
    else:
        print(f"❌ Unsupported file type: {path}")
        return None

    if not dims:
        return None

    orig_w, orig_h = dims
    aspect = orig_w / orig_h

    print(f"\n📄 {path} — original size: {orig_w}x{orig_h} ({aspect:.3f})")
    user_input = input("What width would you like?:")
    target_w = interpret_width_input(user_input)

    if not target_w:
        print("❌ Invalid width input. Skipping...")
        return None

    target_h = int(target_w / aspect)
    print(f"✅ Will add: {path} {target_w}x{target_h}")
    return f"{path} {target_w}x{target_h}"

def main():
    if not os.path.exists(source_file):
        print("❌ sources.txt not found.")
        return

    lines_to_add = []
    with open(source_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            result = process_file(line)
            if result:
                lines_to_add.append(result)

    if lines_to_add:
        with open(output_file, "a") as f:
            for line in lines_to_add:
                f.write(line + "\n")
        print(f"\n✅ {len(lines_to_add)} entries added to {output_file}")

main()
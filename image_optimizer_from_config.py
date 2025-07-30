import os
from PIL import Image
import subprocess

# Accepted image and video extensions
accepted_image_exts = ['.jpg', '.jpeg', '.png', '.webp']
accepted_video_exts = ['.mp4', '.mov', '.avi', '.webm', '.mkv']

def convert_and_resize_image(image_path, width=None, height=None):
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)

    try:
        img = Image.open(image_path)
        original_width, original_height = img.size

        if width and height:
            if original_width < width and original_height < height:
                print(f"Skipping {filename} — original too small for resize.")
                return
            img.thumbnail((width, height))
            out_name = f"{name}-{width}x{height}.webp"
        else:
            out_name = f"{name}.webp"

        out_path = os.path.join("output", out_name)
        img.save(out_path, "WEBP", quality=85)
        print(f"[IMG] Saved {out_path}")
    except Exception as e:
        print(f"[IMG] Error processing {filename}: {e}")

def convert_and_resize_video(video_path, width=None, height=None):
    filename = os.path.basename(video_path)
    name, ext = os.path.splitext(filename)
    out_name = f"{name}.webm"
    out_path = os.path.join("output", out_name)

    scale_filter = ""
    if width and height:
        scale_filter = f",scale={width}:{height}:force_original_aspect_ratio=decrease"

    cmd = [
        "ffmpeg", "-i", video_path,
        "-c:v", "libvpx-vp9", "-crf", "32", "-b:v", "0",
        "-auto-alt-ref", "0",
        "-an",  # no audio
        "-vf", f"fps=30{scale_filter}",
        out_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"[VID] Saved {out_path}")
    except Exception as e:
        print(f"[VID] Error processing {filename}: {e}")

def main():
    input_dir = "input"
    output_dir = "output"
    config_file = "sizes.txt"

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(config_file):
        print("Missing sizes.txt file.")
        return

    with open(config_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            filename = parts[0]
            width = height = None
            if len(parts) == 2:
                try:
                    width, height = map(int, parts[1].lower().split("x"))
                except ValueError:
                    print(f"Invalid size format: {parts[1]}")
                    continue

            full_path = os.path.join(input_dir, filename)
            if not os.path.isfile(full_path):
                print(f"File not found: {full_path}")
                continue

            ext = os.path.splitext(filename)[1].lower()
            if ext in accepted_image_exts:
                convert_and_resize_image(full_path, width, height)
            elif ext in accepted_video_exts:
                convert_and_resize_video(full_path, width, height)
            else:
                print(f"Unsupported file type: {filename}")

if __name__ == "__main__":
    main()

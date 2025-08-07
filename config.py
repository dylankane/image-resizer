import os
from PIL import Image
import subprocess

accepted_image_exts = ['.jpg', '.jpeg', '.png', '.webp']
accepted_video_exts = ['.mp4', '.mov', '.avi', '.webm', '.mkv']
valid_crop_focuses = [
    'center', 'top', 'bottom', 'left', 'right',
    'top-left', 'top-right', 'bottom-left', 'bottom-right'
]

def get_crop_box(src_w, src_h, target_w, target_h, focus):
    aspect_ratio_input = src_w / src_h
    aspect_ratio_target = target_w / target_h

    if aspect_ratio_input > aspect_ratio_target:
        new_width = int(target_h * aspect_ratio_input)
        new_height = target_h
    else:
        new_width = target_w
        new_height = int(target_w / aspect_ratio_input)

    # default center
    left = (new_width - target_w) // 2
    top = (new_height - target_h) // 2

    if 'left' in focus:
        left = 0
    elif 'right' in focus:
        left = new_width - target_w

    if 'top' in focus:
        top = 0
    elif 'bottom' in focus:
        top = new_height - target_h

    return new_width, new_height, left, top

def convert_image(image_path, width=None, height=None, crop_focuses=None):
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)

    try:
        img = Image.open(image_path).convert("RGB")
        original_width, original_height = img.size

        if width and height:
            # Stretched
            stretched = img.resize((width, height))
            out_stretch = os.path.join("output", f"{name}-{width}x{height}-stretch.webp")
            stretched.save(out_stretch, "WEBP", quality=85)
            print(f"[IMG] Saved {out_stretch}")

            for focus in crop_focuses:
                resize_w, resize_h, left, top = get_crop_box(original_width, original_height, width, height, focus)
                resized = img.resize((resize_w, resize_h))
                cropped = resized.crop((left, top, left + width, top + height))
                out_crop = os.path.join("output", f"{name}-{width}x{height}-{focus}-crop.webp")
                cropped.save(out_crop, "WEBP", quality=85)
                print(f"[IMG] Saved {out_crop}")
        else:
            out_path = os.path.join("output", f"{name}.webp")
            img.save(out_path, "WEBP", quality=85)
            print(f"[IMG] Saved {out_path}")

    except Exception as e:
        print(f"[IMG] Error processing {filename}: {e}")

def get_video_crop_filter(width, height, focus):
    x = f"(iw-iw*{width}/{height})/2"
    y = f"(ih-ih*{height}/{width})/2"

    if 'left' in focus:
        x = "0"
    elif 'right' in focus:
        x = f"iw-iw*{width}/{height}"

    if 'top' in focus:
        y = "0"
    elif 'bottom' in focus:
        y = f"ih-ih*{height}/{width}"

    return (
        f"scale='if(gt(a,{width}/{height}),-1,{width})':'if(gt(a,{width}/{height}),{height},-1)',"
        f"crop={width}:{height}:{x}:{y}"
    )

def convert_video(video_path, width=None, height=None, crop_focuses=None):
    filename = os.path.basename(video_path)
    name, ext = os.path.splitext(filename)

    try:
        if width and height:
            # Stretched
            out_stretch = os.path.join("output", f"{name}-{width}x{height}-stretch.webm")
            cmd_stretch = [
                "ffmpeg", "-i", video_path,
                "-vf", f"fps=30,scale={width}:{height}",
                "-c:v", "libvpx-vp9", "-crf", "32", "-b:v", "0",
                "-auto-alt-ref", "0", "-an", out_stretch
            ]
            subprocess.run(cmd_stretch, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"[VID] Saved {out_stretch}")

            for focus in crop_focuses:
                crop_filter = get_video_crop_filter(width, height, focus)
                out_crop = os.path.join("output", f"{name}-{width}x{height}-{focus}-crop.webm")
                cmd_crop = [
                    "ffmpeg", "-i", video_path,
                    "-vf", f"fps=30,{crop_filter}",
                    "-c:v", "libvpx-vp9", "-crf", "32", "-b:v", "0",
                    "-auto-alt-ref", "0", "-an", out_crop
                ]
                subprocess.run(cmd_crop, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                print(f"[VID] Saved {out_crop}")
        else:
            out_path = os.path.join("output", f"{name}.webm")
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vf", "fps=30",
                "-c:v", "libvpx-vp9", "-crf", "32", "-b:v", "0",
                "-auto-alt-ref", "0", "-an", out_path
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"[VID] Saved {out_path}")

    except Exception as e:
        print(f"[VID] Error processing {filename}: {e}")

def main():
    os.makedirs("output", exist_ok=True)
    config_file = "media.txt"

    if not os.path.exists(config_file):
        print("Missing media.txt file.")
        return

    with open(config_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            filepath = parts[0]
            width = height = None
            crop_focuses = ['center']

            if len(parts) >= 2:
                try:
                    width, height = map(int, parts[1].lower().split("x"))
                except ValueError:
                    print(f"Invalid size format: {parts[1]}")
                    continue

            if len(parts) >= 3:
                requested = [p.lower() for p in parts[2:] if p.lower() in valid_crop_focuses]
                if requested:
                    crop_focuses = requested

            if not os.path.isfile(filepath):
                print(f"File not found: {filepath}")
                continue

            ext = os.path.splitext(filepath)[1].lower()
            if ext in accepted_image_exts:
                convert_image(filepath, width, height, crop_focuses)
            elif ext in accepted_video_exts:
                convert_video(filepath, width, height, crop_focuses)
            else:
                print(f"Unsupported file type: {filepath}")

if __name__ == "__main__":
    main()

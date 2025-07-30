# 📦 Image & Video Optimizer Script

A lightweight Python-based tool to **resize and convert images and videos** into web-optimized formats (`.webp`, `.mp4`, `.webm`) for faster loading on modern websites.

---

## 🚀 What It Does

This script:

✅ **Converts images** (`.jpg`, `.jpeg`, `.png`, `.webp`) to `.webp`  
✅ **Converts videos** (`.mp4`, `.mov`, `.avi`, etc.) to `.webm`  
✅ **Resizes images and videos** only if resize dimensions are provided  
✅ **Keeps original quality** when no resizing is needed  
✅ **Skips processing** if files are already too small  
✅ **Saves optimized files** to an `/output` folder  
✅ Uses **Pillow** for image processing and **FFmpeg** for video conversion

---

## 🧰 Requirements

- **Python 3.7+**
- **Pillow** (for images):  
  Install with: `pip install pillow`
- **FFmpeg** (for videos):  
  [Download here](https://www.gyan.dev/ffmpeg/builds/) → Add the `/bin` folder to your system PATH

---

## 📁 Folder Structure

image-resizer/
│
├── input/ ← Place original images/videos here
├── output/ ← Optimized files will appear here
├── sizes.txt ← Configuration file (see below)
├── optimizer.py ← The main script


---

## ✍️ How to Use

### 1. Add media to the `input/` folder

Put your raw `.jpg`, `.png`, `.mp4`, etc. files into the `input/` folder.

---

### 2. Create or edit `sizes.txt`

This file tells the script **what to convert and what to resize**.

#### ✅ Resize + convert

home-hero.jpg 1920x1080
product.jpg 500x500
promo-video.mp4 1280x720

#### ✅ Convert only (no resizing)

icon.png
gallery.mp4


You can **mix both styles** in one file.

---

### 3. Run the script

From your terminal:

```bash
python image_optimizer_from_config.py
```

All optimized files will appear in the output/ folder.

💡 Output Behavior
Type	Input File	Output Format	Resize Optional?	Compression
Image	.jpg, .png	.webp	✅ Yes	Yes (via Pillow)
Video	.mp4, .avi	.webm	✅ Yes	Yes (via FFmpeg)

If no dimensions are provided, it converts as-is.

Output files are named like: filename-500x500.webp or video-1280x720.webm.

🔍 Troubleshooting
🛠 Make sure FFmpeg is installed and added to your system PATH.

🧪 Check that filenames in sizes.txt match exactly (case-sensitive).

🧼 Script skips unsupported files or formats that are too small to resize.

 License
MIT — Free to use, modify, and share


---

Let me know if you want the script name updated or if you'd like a badge-style version for GitHub display!

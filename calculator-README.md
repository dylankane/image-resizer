# 📐 Aspect Ratio Resize Calculator (CLI Tool)

This command-line tool helps you generate perfectly sized media entries for `media.txt` **without changing aspect ratio**.

---

## 🚀 How It Works

1. Put your file paths into `sources.txt`:
```
input/photo.jpg
input/clip.mp4
```

2. Run:
```
python aspect_calculator.py
```

3. For each file, it will:
   - Read the original dimensions
   - Ask: **"What width would you like?"**

4. You can answer with:
   - `800px` → fixed width
   - `50%` → 50% of 1440px (default screen width)
   - `50% small` → 50% of 768px (small-screen mode)
   - `grid`, `thumbnail`, `logo`, `main`, `hero`, `full` → preset widths

5. The script writes this to `media.txt`:
```
input/photo.jpg 800x533
```

---

## 📊 Presets

| Preset     | Width (px) |
|------------|------------|
| logo       | 200        |
| thumbnail  | 400        |
| grid       | 800        |
| main       | 1200       |
| hero       | 1600       |
| full       | 1920       |

---

## 🧠 Notes

- Aspect ratio is preserved automatically
- Videos use `ffprobe` (make sure it's installed)
- All entries are appended to `media.txt`

---

# 📸 Media Resizer & Converter

This is a simple but powerful tool for converting and resizing **images and videos**. It produces multiple versions of each file:
- A **stretched** version (resized exactly to your requested dimensions)
- One or more **cropped** versions based on your crop focus (e.g. top, center, bottom, etc.)

All resized files are saved in `output/`, ready for web or app use.

---

## 🚀 How to Use the App (Step-by-Step)

### 1. Place your media files
Put all images and videos into the `input/` folder.  
Supported formats:
- **Images**: `.jpg`, `.jpeg`, `.png`, `.webp`
- **Videos**: `.mp4`, `.mov`, `.avi`, `.webm`, `.mkv`

### 2. Open `media.txt` and define what to convert

For each media file you want to process:

- Go to the `input/` folder
- **Right-click the file and choose "Copy"**
- Open `media.txt` and **paste** into a new line
- Then add the **desired size** and any **crop focus options** you want

#### 📝 Example lines:
```
input/photo.jpg 500x800 top center bottom
input/video.mp4 720x1280 bottom-right
input/logo.png
```

### 3. Run the script

In the terminal, from the project folder, run:

```
python config.py
```

---

## 📦 What You’ll Get

For each file:

✅ A `-stretch` version (forced into the new dimensions)  
✅ One `-crop` version **per** crop focus — cropped and centered to your target shape

**Example:**

```
input/photo.jpg 500x800 top bottom
```

Outputs:
- `photo-500x800-stretch.webp`
- `photo-500x800-top-crop.webp`
- `photo-500x800-bottom-crop.webp`

For videos, the output format is `.webm`.

---

## 🧠 What the Script Actually Does

- Reads instructions from `media.txt`
- For each media file:
  - If no size is given → convert to `.webp` or `.webm` only
  - If a size is given:
    - Create **one stretched version**
    - Create **one cropped version per crop focus**
- All output is saved to the `/output/` folder
- Crops preserve visual proportions without distortion
- Stretching forces the image or video into the exact shape, even if distorted

---

## 💻 How to Access the Application (No Experience Needed)

This script can be run using **free tools** with no installation required. You can either **clone** or **fork** the repository:

- **Fork**: Makes your own copy of the repo under your GitHub account. Use this if you want to edit the script or save your work.
- **Clone**: Makes a temporary copy on your local machine or editor, but does not save changes back to GitHub unless you push them.

---

### ✅ Option 1: Use GitHub Codespaces *(Free on personal GitHub accounts)*

1. Log into [https://github.com](https://github.com)
2. Go to the repository and click **Fork** (top-right) to make your own copy
3. On your new fork, click the green **Code** button > **Open in Codespaces**
4. Wait for the cloud IDE to load
5. Inside the built-in terminal, run:

```
python config.py
```

---

### ✅ Option 2: Use Replit *(Free browser-based IDE)*

1. Go to [https://replit.com](https://replit.com)
2. Click **+ Create Repl** > **Import from GitHub**
3. Paste the GitHub repo URL
4. Wait for it to load
5. Use the left panel to:
   - Upload media files to the `input/` folder
   - Open and edit `media.txt`
6. In the console at the bottom, run:

```
python config.py
```

---

### ✅ Option 3: Run locally using VS Code

1. Download and install:
   - [VS Code](https://code.visualstudio.com/)
   - [Python](https://www.python.org/downloads/)
2. Open VS Code
3. Open the project folder you downloaded or cloned
4. Use the built-in terminal to run:

```
python config.py
```

---

## 🧾 Crop Focus Options (for more control)

| Focus         | Description             |
|---------------|--------------------------|
| `center`      | (default) Centered crop  |
| `top`         | Crop toward the top      |
| `bottom`      | Crop toward the bottom   |
| `left`        | Crop toward the left     |
| `right`       | Crop toward the right    |
| `top-left`    | Crop top-left corner     |
| `top-right`   | Crop top-right corner    |
| `bottom-left` | Crop bottom-left corner  |
| `bottom-right`| Crop bottom-right corner |

You can list **multiple** crop focuses for a single file:
```
input/header.jpg 500x300 top bottom center
```

---

## 🙋 FAQ

**Q: Will it stretch the media?**  
Yes — it makes one stretched version per file.

**Q: Will it crop the image to the shape I need?**  
Yes — and lets you choose where to crop from.

**Q: Can I delete the outputs I don’t like?**  
Yes — every output is standalone. Just delete the ones you don’t need.

---


# 🔁 CopyShapeKeyWhatEver – Shape Key Transfer Tool for Blender

A Blender add-on that allows you to copy shape keys (morph targets) between objects, even if they have **completely different topology or UVs**.

Originally built to transfer **facial animations** between characters, but works with **any morphs**.

---

## 🧩 Features

### ✅ Same Topology (Manual Transfer)
- Select `Source` (high-poly with morphs)
- Select `Target` (low-poly or duplicate)
- Check scale and alignment
- Filter which morphs to transfer by prefix
- Automatically merge duplicates and clean up

### ⚙️ Different Topology (Surface Deform)
- Transfer shape keys from any object to another, regardless of topology
- Uses `Surface Deform` modifier under the hood
- Clean UI and console error feedback
- No UVs required

---

## 📷 UI Overview

![UI Screenshot](your-screenshot-file-name.png)

---

## 💻 Installation

1. Download `copy_shape_key_whatever.py`
2. In Blender, go to **Edit → Preferences → Add-ons → Install**
3. Select the file and enable the add-on

---

## 🚀 Usage

### Same Topology
- Select source and target meshes
- Follow steps 1–3
- Filter morphs by prefix or leave empty to transfer all
- Merge the result

### Different Topology
- Choose Hi-poly and Lo-poly objects
- Optionally enter prefix to filter shape keys
- Click `Copy Shape Keys (Surface Deform)`

---

## 📂 Files

- `copy_shape_key_whatever.py` — the Blender add-on
- `README.md` — you're reading it
- *(Optional)* `LICENSE` — default: MIT or "Demo Only"
- *(Optional)* `/images/` — contains UI screenshot

---

## 🛠 Requirements

- Blender 3.x+
- No external Python dependencies

---

## 🧠 How It Works (Concept)

The add-on handles two use cases:
- For identical topology: native shape key copying and cleanup
- For different topology: uses `Surface Deform` to bake deformation from source to target, then converts that to shape keys

---

## 📄 License

This public version is available for non-commercial use and demonstration purposes.  
Author reserves the right to revoke or restrict usage at any time.

---

## 👤 Author

Created by a 3D artist for personal production workflows.  
If you want to contribute, feel free to open a pull request or issue.


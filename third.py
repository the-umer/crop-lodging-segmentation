import os
import shutil
import random

# ===== PATHS =====
IMG_DIR = "dataset/images"
MASK_DIR = "dataset/masks"

OUT_DIR = "dataset_split"

train_img = os.path.join(OUT_DIR, "train/images")
train_mask = os.path.join(OUT_DIR, "train/masks")

val_img = os.path.join(OUT_DIR, "val/images")
val_mask = os.path.join(OUT_DIR, "val/masks")

# create folders
for p in [train_img, train_mask, val_img, val_mask]:
    os.makedirs(p, exist_ok=True)

# ===== GET FILES =====
files = os.listdir(IMG_DIR)
random.shuffle(files)

split = int(0.8 * len(files))

train_files = files[:split]
val_files = files[split:]

print("Train:", len(train_files))
print("Val:", len(val_files))

# ===== COPY FUNCTION =====
def copy_pair(file_list, img_dst, mask_dst):
    for f in file_list:
        img_path = os.path.join(IMG_DIR, f)

        base = os.path.splitext(f)[0]

        # find corresponding mask
        mask_path = None
        for ext in [".png", ".jpg"]:
            p = os.path.join(MASK_DIR, base + ext)
            if os.path.exists(p):
                mask_path = p
                break

        if mask_path is None:
            print("⚠️ Missing mask for:", f)
            continue

        shutil.copy(img_path, os.path.join(img_dst, f))
        shutil.copy(mask_path, os.path.join(mask_dst, os.path.basename(mask_path)))

# ===== SPLIT =====
copy_pair(train_files, train_img, train_mask)
copy_pair(val_files, val_img, val_mask)

print("✅ Dataset split completed successfully!")
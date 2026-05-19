import os
import shutil

BASE = "/Users/umerkhayammir/Desktop/Crop Lodging.v2i.coco-segmentation 2"

IMG_SRC = [
    "train",
    "augmented/images"
]

MASK_SRC = [
    "masks",
    "augmented/masks"
]

IMG_DST = "dataset/images"
MASK_DST = "dataset/masks"

os.makedirs(IMG_DST, exist_ok=True)
os.makedirs(MASK_DST, exist_ok=True)

# copy images
for folder in IMG_SRC:
    path = os.path.join(BASE, folder)
    for f in os.listdir(path):
        shutil.copy(os.path.join(path, f), os.path.join(IMG_DST, f))

# copy masks
for folder in MASK_SRC:
    path = os.path.join(BASE, folder)
    for f in os.listdir(path):
        shutil.copy(os.path.join(path, f), os.path.join(MASK_DST, f))

print("✅ Merge complete")
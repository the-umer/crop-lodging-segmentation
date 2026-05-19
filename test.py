import json
import os
import cv2
import numpy as np
from tqdm import tqdm

# paths
ANNOTATION_FILE = "/Users/umerkhayammir/Desktop/Crop Lodging.v2i.coco-segmentation 2/train/_annotations.coco.json"
IMAGE_DIR = "images"
OUTPUT_MASK_DIR = "masks"

os.makedirs(OUTPUT_MASK_DIR, exist_ok=True)

# load json
with open(ANNOTATION_FILE) as f:
    coco = json.load(f)

# create image_id → filename mapping
image_info = {img["id"]: img for img in coco["images"]}

# group annotations by image
ann_by_image = {}
for ann in coco["annotations"]:
    img_id = ann["image_id"]
    ann_by_image.setdefault(img_id, []).append(ann)

# process each image
for img_id, anns in tqdm(ann_by_image.items()):
    img_data = image_info[img_id]
    h, w = img_data["height"], img_data["width"]
    
    # create empty mask
    mask = np.zeros((h, w), dtype=np.uint8)

    for ann in anns:
        if "segmentation" not in ann:
            continue
        
        for seg in ann["segmentation"]:
            polygon = np.array(seg).reshape(-1, 2).astype(np.int32)
            cv2.fillPoly(mask, [polygon], 255)

    # save mask
    filename = img_data["file_name"]
    mask_name = os.path.splitext(filename)[0] + ".png"
    cv2.imwrite(os.path.join(OUTPUT_MASK_DIR, mask_name), mask)

print("Masks generated successfully!")
import os
import cv2
from tqdm import tqdm
import albumentations as A

# -----------------------------
# STEP 1: Define paths
# -----------------------------
image_dir = "train"
mask_dir = "masks"

output_img_dir = "augmented/images"
output_mask_dir = "augmented/masks"

os.makedirs(output_img_dir, exist_ok=True)
os.makedirs(output_mask_dir, exist_ok=True)

# -----------------------------
# STEP 2: Debug info
# -----------------------------
print("Working directory:", os.getcwd())

image_files = sorted(os.listdir(image_dir))
mask_files = sorted(os.listdir(mask_dir))

print("Total images:", len(image_files))
print("Total masks:", len(mask_files))

# -----------------------------
# STEP 3: Define augmentation
# ----------------------------- 
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.3),
    A.RandomRotate90(p=0.5),

    A.Affine(
        translate_percent=0.05,
        scale=(0.8, 1.2),
        rotate=(-20, 20),
        p=0.5
    ),

    A.RandomBrightnessContrast(p=0.4),
    A.GaussianBlur(p=0.2),

], additional_targets={'masks': 'masks'})

# -----------------------------
# STEP 4: Target size
# -----------------------------
target_size = 2200
current_count = len(image_files)

print("Starting augmentation...")
print("Current:", current_count, "Target:", target_size)

i = 0

# -----------------------------
# STEP 5: Augmentation loop
# -----------------------------
while current_count < target_size:
    for img_name in tqdm(image_files):

        img_path = os.path.join(image_dir, img_name)

        # FIX: match mask filename
        mask_name = os.path.splitext(img_name)[0] + ".png"
        mask_path = os.path.join(mask_dir, mask_name)

        # check if mask exists
        if not os.path.exists(mask_path):
            print("❌ Mask missing:", mask_name)
            continue

        # read image & mask
        image = cv2.imread(img_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print("❌ Image failed:", img_name)
            continue

        if mask is None:
            print("❌ Mask failed:", mask_name)
            continue

        # apply augmentation
        augmented = transform(image=image, mask=mask)

        aug_img = augmented["image"]
        aug_mask = augmented["mask"]

        # save new files
        new_name = f"aug_{i}_{img_name}"

        cv2.imwrite(os.path.join(output_img_dir, new_name), aug_img)
        cv2.imwrite(os.path.join(output_mask_dir, new_name), aug_mask)

        i += 1
        current_count += 1

        if current_count >= target_size:
            break

print("✅ Augmentation completed!")
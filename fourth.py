import os

# ===== PATHS =====
base_path = "dataset_split"

splits = ["train", "val"]

for split in splits:
    img_dir = os.path.join(base_path, split, "images")
    mask_dir = os.path.join(base_path, split, "masks")

    images = sorted(os.listdir(img_dir))
    masks = sorted(os.listdir(mask_dir))

    print(f"\nProcessing {split} set:")
    print(f"Images: {len(images)}, Masks: {len(masks)}")

    # Create mapping based on filename without extension
    img_dict = {os.path.splitext(f)[0]: f for f in images}
    mask_dict = {os.path.splitext(f)[0]: f for f in masks}

    common_keys = sorted(set(img_dict.keys()) & set(mask_dict.keys()))

    print(f"Matched pairs: {len(common_keys)}")

    for idx, key in enumerate(common_keys):
        new_name = f"{idx:04d}"

        img_old = os.path.join(img_dir, img_dict[key])
        mask_old = os.path.join(mask_dir, mask_dict[key])

        img_ext = os.path.splitext(img_dict[key])[1]
        mask_ext = os.path.splitext(mask_dict[key])[1]

        img_new = os.path.join(img_dir, new_name + img_ext)
        mask_new = os.path.join(mask_dir, new_name + mask_ext)

        os.rename(img_old, img_new)
        os.rename(mask_old, mask_new)

    # Report unmatched files
    unmatched_imgs = set(img_dict.keys()) - set(mask_dict.keys())
    unmatched_masks = set(mask_dict.keys()) - set(img_dict.keys())

    print(f"Unmatched images: {len(unmatched_imgs)}")
    print(f"Unmatched masks: {len(unmatched_masks)}")
    
print(images[:5])
print(masks[:5])
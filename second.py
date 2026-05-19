import os

IMG_DIR = "dataset/images"
MASK_DIR = "dataset/masks"

img_files = os.listdir(IMG_DIR)
mask_files = os.listdir(MASK_DIR)

# convert to base names
img_names = set(os.path.splitext(f)[0] for f in img_files)
mask_names = set(os.path.splitext(f)[0] for f in mask_files)

# find missing
missing = img_names - mask_names

print("Total missing:", len(missing))

# print full list
for name in missing:
    print(name)
    
    print("Will delete:")
    
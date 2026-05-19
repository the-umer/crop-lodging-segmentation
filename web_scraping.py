import os
import requests
from bs4 import BeautifulSoup
import urllib.parse

# ===== CONFIG =====
QUERY = "UAV crop lodging images"
NUM_IMAGES = 100
SAVE_DIR = "crop_lodging_images"

# ===== CREATE FOLDER =====
os.makedirs(SAVE_DIR, exist_ok=True)

# ===== BUILD SEARCH URL =====
query_encoded = urllib.parse.quote(QUERY)
url = f"https://www.bing.com/images/search?q={query_encoded}&FORM=HDRSC2"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ===== REQUEST PAGE =====
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# ===== EXTRACT IMAGE LINKS =====
image_elements = soup.find_all("a", class_="iusc")

image_urls = []
for elem in image_elements:
    try:
        m = elem.get("m")
        start = m.find('"murl":"') + 8
        end = m.find('"', start)
        img_url = m[start:end]
        image_urls.append(img_url)
    except:
        continue

# ===== DOWNLOAD IMAGES =====
count = 0
for i, img_url in enumerate(image_urls):
    if count >= NUM_IMAGES:
        break
    try:
        img_data = requests.get(img_url, timeout=5).content
        file_path = os.path.join(SAVE_DIR, f"image_{count}.jpg")

        with open(file_path, "wb") as f:
            f.write(img_data)

        print(f"Downloaded {count+1}")
        count += 1

    except Exception as e:
        print(f"Failed: {img_url}")

print("Done!")
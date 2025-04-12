import urllib.request, json
import secret
import time
from io import BytesIO
from PIL import Image
import os
import shutil
from pynput import keyboard
from rich_pixels import Pixels
from rich.console import Console

# for i in range(259, 1000):
#     time.sleep(2)
#     try:
#         url = f"https://api.odot.state.or.us/tripcheck/Cctv/Inventory?DeviceId={i}"

#         hdr ={
#         # Request headers
#         'Cache-Control': 'no-cache',
#         'Ocp-Apim-Subscription-Key': secret.getKey(),
#         }

#         req = urllib.request.Request(url, headers=hdr)

#         req.get_method = lambda: 'GET'
#         response = urllib.request.urlopen(req)
#         r_code = response.getcode()
#         r_text = json.loads(response.read().decode('utf-8'))
#         if r_code == 200:
#             file = open("valid_ids.txt", "a")
#             file.write(f"{r_text['CCTVInventoryRequest'][0]['device-id']},")
#             file.close()
#     except Exception as e:
#         print(f"Error: {e}, {i}")

# n = 0
# while True:
#     for i in secret.get_valid_ids():
#         time.sleep(2)
#         try:
#             url = f"https://api.odot.state.or.us/tripcheck/Cctv/Inventory?DeviceId={i}"
#             hdr = {
#                 # Request headers
#                 'Cache-Control': 'no-cache',
#                 'Ocp-Apim-Subscription-Key': secret.get_key(),
#             }
#             req = urllib.request.Request(url, headers=hdr)
#             req.get_method = lambda: 'GET'
#             response = urllib.request.urlopen(req)
#             r_code = response.getcode()
#             r_text = json.loads(response.read().decode('utf-8'))
#             url = r_text['CCTVInventoryRequest'][0]['cctv-url'].replace(' ', '%20')
#             image_response = urllib.request.urlopen(url)
#             image_data = image_response.read()
#             image = Image.open(BytesIO(image_data))
#             width, height = image.size
#             cropped_image = image.crop((5, 40, width - 5, height - 50))
#             cropped_image.save(f"./imgs/device_{i}_{n}.jpg", "JPEG")
#             n += 1
#             print(f"Saved image for device {i}: {n}")
#         except Exception as e:
#             print(f"Error: {e}, {i}")

for i in range(1):
    imgs_dir = "./imgs/"
    positive_dir = "./positive/"
    negative_dir = "./negative/"

    os.makedirs(positive_dir, exist_ok=True)
    os.makedirs(negative_dir, exist_ok=True)

    images = [img for img in os.listdir(imgs_dir) if img.endswith(".jpg")]
    current_index = 0

    def on_press(key):
        global current_index
        try:
            if key == keyboard.Key.right:  # Move to positive
                shutil.move(os.path.join(imgs_dir, images[current_index]), positive_dir)
                print(f"Moved to positive: {images[current_index]}")
                current_index += 1
            elif key == keyboard.Key.left:  # Move to negative
                shutil.move(os.path.join(imgs_dir, images[current_index]), negative_dir)
                print(f"Moved to negative: {images[current_index]}")
                current_index += 1
            elif key == keyboard.Key.up:  # Delete image
                os.remove(os.path.join(imgs_dir, images[current_index]))
                print(f"Deleted: {images[current_index]}")
                current_index += 1
            if current_index >= len(images):
                print("No more images.")
                return False  # Stop listener
            display_image()
        except Exception as e:
            print(f"Error: {e}")

    def display_image():
        console = Console()
        img_path = os.path.join(imgs_dir, images[current_index])
        pixels = Pixels.from_image_path(img_path)  # Increase resolution for better quality
        console.print(pixels)


    if images:
        display_image()
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    else:
        print("No images found in the directory.")
import moondream as md
import requests
from PIL import Image
import os.path
import time

start_time = time.time()

if os.path.isfile("D:\\apk1\\imgrecpy\\uploads\\photo.jpg"):
    model = md.vl(model="D:\\apk1\\moondream-2b-int8.mf")

    # Apri immagine e processala
    image = Image.open("D:\\apk1\\imgrecpy\\uploads\\photo.jpg")
    encoded_image = model.encode_image(image)

    # Genera didascalia (INGLESE)
    caption = model.caption(encoded_image)["caption"]
    print("Caption:", caption)
    
    with open('filename.txt', 'w') as fp:
        fp.write(caption)

    with open('filename.txt', "rb") as file:
        files = {"file": file}
        response = requests.post("http://192.168.138.248:5000/upload", files=files)

    print("--- %s seconds ---" % (time.time() - start_time))
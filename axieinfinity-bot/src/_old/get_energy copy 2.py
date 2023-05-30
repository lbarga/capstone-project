from PIL import Image
import pytesseract
from ppadb.client import Client as AdbClient
import os
import shutil

host = "127.0.0.1"
port = 5037
tmp_images_path = './tmp_images'
image_path = '/image.png'
resized_image_path = '/resized_image.png'


def create_tmp_images_folder():
    os.mkdir(tmp_images_path)


def delete_tmp_images_folder():
    shutil.rmtree(tmp_images_path)

delete_tmp_images_folder()

create_tmp_images_folder()

client = AdbClient(host=host, port=port)

devices = client.devices()

device = devices[0]

image = device.screencap()


with open(tmp_images_path + image_path, 'wb') as f:
    f.write(image)

image = Image.open(tmp_images_path + image_path)

# ARENA_BTN
# left = 1230
# top = 480
# right = 1450
# bottom = 560

left = 40
right = 57
top = 566
bottom = 585

croped_image = image.crop((left, top, right, bottom))

width, height = croped_image.size

zoom = 10

resized_image = croped_image.resize((width*zoom, height*zoom))


resized_image.save(tmp_images_path + resized_image_path)

string = pytesseract.image_to_string(resized_image)

print(string)

split = string.split('/')

for i, v in enumerate(split):
    split[i] = v.replace('\n\x0c', '')

device.input_tap(1500, 400)

print(split)



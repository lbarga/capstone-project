from PIL import Image
import pytesseract
from ppadb.client import Client as AdbClient
import os
import shutil
import time

host = "127.0.0.1"
port = 5037
tmp_images_path = './tmp-images'
image_path = '/image.png'
resized_image_path = '/resized-image.png'


def create_tmp_images_folder():
    os.mkdir(tmp_images_path)


def delete_tmp_images_folder():
    shutil.rmtree(tmp_images_path)


def enter_in_adventure_surrender_and_return_home():
    device.input_tap(1300, 400)
    device.input_tap(470, 175)
    device.input_tap(1120, 620)
    time.sleep(7)
    device.input_tap(1490, 40)
    device.input_tap(770, 445)
    device.input_tap(680, 420)
    time.sleep(5)
    device.input_tap(100, 550)
    device.input_tap(100, 550)
    time.sleep(5)
    device.input_tap(50, 45)


while True:
    create_tmp_images_folder()

    client = AdbClient(host=host, port=port)

    devices = client.devices()

    device = devices[0]

    image = device.screencap()

    with open(tmp_images_path + image_path, 'wb') as f:
        f.write(image)

    image = Image.open(tmp_images_path + image_path)

    left = 120
    top = 110
    right = 180
    bottom = 125

    croped_image = image.crop((left, top, right, bottom))

    width, height = croped_image.size

    zoom = 4

    resized_image = croped_image.resize((width*zoom, height*zoom))

    resized_image.save(tmp_images_path + resized_image_path)

    string = pytesseract.image_to_string(resized_image)

    split = string.split('/')

    for i, v in enumerate(split):
        split[i] = v.replace('\n\x0c', '')

    enter_in_adventure_surrender_and_return_home()

    print(split)

    delete_tmp_images_folder()

# command to put cards
# adb shell  "input touchscreen swipe 240 600 240 300"
# adb shell  "input touchscreen swipe 610 600 610 300"

from PIL import Image
import pytesseract
from ppadb.client import Client as AdbClient
import os
import shutil

host = "127.0.0.1"
port = 5037
image_path = 'screenshot.png'

client = AdbClient(host=host, port=port)

devices = client.devices()

device = devices[0]

device.shell('input touchscreen swipe 350 615 350 315')

image = device.screencap()

with open(image_path, 'wb') as f:
    f.write(image)

from PIL import Image
import pytesseract
from ppadb.client import Client as AdbClient
import os
import shutil
import cv2

host = "127.0.0.1"
port = 5037
image_path = 'screenshot.png'

client = AdbClient(host=host, port=port)

devices = client.devices()

device = devices[0]

image = device.screencap()

with open(image_path, 'wb') as f:
    f.write(image)

img = cv2.imread(image_path)

# img = img[370:420, 1235:1420] # ADVENTURE
# img = img[500:525, 1425:1510] # END TURN
# img = img[591:604, 225:242]  # DAMAGE_CARD

scale_percent = 500

width = int(img.shape[1] * scale_percent / 100)

height = int(img.shape[0] * scale_percent / 100)

dim = (width, height)

img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

print(pytesseract.image_to_string(img))

cv2.imshow('Result', img)

cv2.waitKey(0)

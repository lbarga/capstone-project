from PIL import Image
import pytesseract
from ppadb.client import Client as AdbClient
import cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

client = AdbClient(host="127.0.0.1", port=5037)

devices = client.devices()

device = devices[0]

image = device.screencap()

with open('image.png', 'wb') as f:
    f.write(image)

image = Image.open('./image.png')

left = 120
top = 110
right = 180
bottom = 130

croped_image = image.crop((left, top, right, bottom)) 

width, height = croped_image.size

resized_image = croped_image.resize((width*4, height*4))

resized_image.save('resized_image.png')

string = pytesseract.image_to_string(resized_image)

print(string)

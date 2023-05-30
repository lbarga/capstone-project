from PIL import Image
import pytesseract
from ppadb.client import Client as AdbClient
import os
import shutil


image = Image.open('../assets/new_energy.png')

left = 290
right = 485
top = 315
bottom = 425

croped_image = image.crop((left, top, right, bottom))

width, height = croped_image.size

print(width,height)

zoom = 5

resized_image = croped_image.resize((width*zoom, height*zoom))

resized_image.save('tmp_energy.png')

string = pytesseract.image_to_string(resized_image)

print(string)

split = string.split('/')

for i, v in enumerate(split):
    split[i] = v.replace('\n\x0c', '')

print(split)



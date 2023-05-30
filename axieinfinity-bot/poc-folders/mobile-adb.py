from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)

devices = client.devices()

print(devices)

apk_path = 'C:/aptoide.apk'

device = devices[0]

image = device.screencap()

with open('screen.jpg', 'wb') as f:
    f.write(image)
    



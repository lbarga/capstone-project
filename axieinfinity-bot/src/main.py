import cv2 as cv
import numpy as np
import os
from ppadb.client import Client as AdbClient
import logging
import threading
import time

os.system('adb start-server')

HOST = "127.0.0.1"
PORT = 5037
client = AdbClient(host=HOST, port=PORT)

_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=_format, level=logging.INFO, datefmt="%H:%M:%S")


def auto_verification(auto_verification_device):
    screen_path = 'screenshots/screenshot-' + auto_verification_device.get_serial_no() + '-verification.png'
    verify_button_path = 'assets/verify-button.png'

    image = auto_verification_device.screencap()

    with open(screen_path, 'wb') as f:
        f.write(image)

    screen_image = cv.imread(screen_path, cv.IMREAD_UNCHANGED)
    screen_gray = cv.cvtColor(screen_image, cv.COLOR_BGR2GRAY)

    verify_button_image = cv.imread(verify_button_path, cv.IMREAD_UNCHANGED)
    verify_button_gray = cv.cvtColor(verify_button_image, cv.COLOR_BGR2GRAY)

    method = cv.TM_CCOEFF_NORMED

    result = cv.matchTemplate(screen_gray, verify_button_gray, method)

    locations = np.where(result >= 0.75)

    locations = list(zip(*locations[::-1]))

    rectangles = []

    needle_w = verify_button_gray.shape[1]
    needle_h = verify_button_gray.shape[0]

    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles = cv.groupRectangles(
        rectangles, groupThreshold=1, eps=0.5)[0]

    if len(rectangles) > 0:
        verify_button_position = rectangles[0]
        position_x = verify_button_position[0]
        position_y = verify_button_position[1]
        auto_verification_device.input_tap(position_x, position_y + 20)
        print("=====verified=====")
    else:
        1+1

def detect_on_image(need_img_path, screen_img_path, threshold=0.5):
    screen_img = cv.imread(screen_img_path, cv.IMREAD_UNCHANGED)
    need_img = cv.imread(need_img_path, cv.IMREAD_UNCHANGED)
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(screen_img, need_img, method)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    rectangles = []

    needle_w = need_img.shape[1]
    needle_h = need_img.shape[0]

    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles = cv.groupRectangles(
        rectangles, groupThreshold=1, eps=0.5)[0]

    return rectangles


def put_cards(rectangles, put_card_device):
    for index, rectangle in enumerate(rectangles):
        position_x = rectangle[0]
        position_y = rectangle[1]

        command = 'input touchscreen swipe ' + \
                  str(position_x + 50) + ' ' + str(position_y + 50) + ' ' + \
                  str(position_x + 50) + ' ' + str(position_y + 50 - 300)

        put_card_device.shell(command)

        if index == len(rectangles) - 1:
            put_card_device.input_tap(1450, 510)


def run_script(run_device):

    image_path = 'screenshots/screenshot-' + run_device.get_serial_no() + '.png'
    card_path = 'assets/card.png'
    
    time.sleep(1)

    image = run_device.screencap()

    with open(image_path, 'wb') as f:
        f.write(image)

    cards = detect_on_image(card_path, image_path)

    cards_count = len(cards)

    if cards_count > 0:
        print(run_device.get_serial_no() + ' detected cards: ' + str(cards_count))
        time.sleep(0.1)
        put_cards(cards, run_device)
        time.sleep(10)
    else:
        print(run_device.get_serial_no() + ' no have cards')

        class Modes:
            ADVENTURE = (1125, 625)
            ARENA = (1315, 515)
            DEFAULT = (710, 630)

        button_position = Modes.DEFAULT
        button_tag = 'nowhere'

        arena_button_path = 'assets/arena.png'
        screen_img = cv.imread(image_path, cv.IMREAD_UNCHANGED)
        screen_img = cv.cvtColor(screen_img, cv.COLOR_BGR2GRAY)
        need_img = cv.imread(arena_button_path, cv.IMREAD_UNCHANGED)
        need_img = cv.cvtColor(need_img, cv.COLOR_BGR2GRAY)
        method = cv.TM_CCOEFF_NORMED
        result = cv.matchTemplate(screen_img, need_img, method)
        locations = np.where(result >= 0.75)
        locations = list(zip(*locations[::-1]))
        arena_rectangles = []
        needle_w = need_img.shape[1]
        needle_h = need_img.shape[0]
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
            arena_rectangles.append(rect)
            arena_rectangles.append(rect)
        arena_rectangles = cv.groupRectangles(arena_rectangles, groupThreshold=1, eps=0.5)[0]
        if len(arena_rectangles) > 0:
            button_tag = 'ARENA'
            button_position = Modes.ARENA

        adventure_button_path = 'assets/adventure.png'
        screen_img = cv.imread(image_path, cv.IMREAD_UNCHANGED)
        screen_img = cv.cvtColor(screen_img, cv.COLOR_BGR2GRAY)
        need_img = cv.imread(adventure_button_path, cv.IMREAD_UNCHANGED)
        need_img = cv.cvtColor(need_img, cv.COLOR_BGR2GRAY)
        method = cv.TM_CCOEFF_NORMED
        result = cv.matchTemplate(screen_img, need_img, method)
        locations = np.where(result >= 0.75)
        locations = list(zip(*locations[::-1]))
        arena_rectangles = []
        needle_w = need_img.shape[1]
        needle_h = need_img.shape[0]
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
            arena_rectangles.append(rect)
            arena_rectangles.append(rect)
        arena_rectangles = cv.groupRectangles(arena_rectangles, groupThreshold=1, eps=0.5)[0]
        if len(arena_rectangles) > 0:
            button_tag = 'ADVENTURE'
            button_position = Modes.ADVENTURE

        if button_position:
            print('Enter in ' + button_tag)
            (position_x, position_y) = button_position
            run_device.input_tap(position_x, position_y)


def thread_function(thread_device):
    while True:
        print('Devices: ', len(thread_devices))
        run_script(thread_device)


def thread_verification_function(thread_verification_function_device):
    while True:
        auto_verification(thread_verification_function_device)


thread_devices = list()

while True:
    try:
        devices = client.devices()
        devices_serial_no = list()

        if len(devices) > 0:
            for device in devices:
                device_serial_no = device.get_serial_no()
                devices_serial_no.append(device_serial_no)

                if device_serial_no not in thread_devices:
                    thread_devices.append(device_serial_no)
                    thread_bot = threading.Thread(target=thread_function, args=(device,))
                    thread_bot.start()
                    thread_verification = threading.Thread(target=thread_verification_function, args=(device,))
                    thread_verification.start()

            not_in_threaded = list(set(thread_devices) ^ set(devices_serial_no))

            for threaded in not_in_threaded:
                thread_devices.remove(threaded)
        else:
            thread_devices = []
            print('===no cell connected===')
            time.sleep(1)
    except:
        1 + 1

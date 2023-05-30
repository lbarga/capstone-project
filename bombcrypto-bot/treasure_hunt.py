from detection import *
from mouse import *


in_treasure_hunt = False

def in_treasure_hunt_screen():
    return detect_image_location('samples/treasure-hunt-back-button.png')

def enter_in_treasure_hunt():
    global in_treasure_hunt

    treasure_hunt_button = detect_image_location('samples/treasure-hunt-button.png')

    if treasure_hunt_button.exist:
        in_treasure_hunt = True
        mouse_click(treasure_hunt_button.position)


def exit_treasure_hunt_screen():
    global in_treasure_hunt

    treasure_hunt_back_button = detect_image_location('samples/treasure-hunt-back-button.png')

    if treasure_hunt_back_button.exist:
        in_treasure_hunt = False
        mouse_click(treasure_hunt_back_button.position)

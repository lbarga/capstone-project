from detection import *
from mouse import *
from screen import *


login_button_clicked = False

def in_login_screen():
    return detect_image_location('samples/login-button.jpg')

def login(login_screen_button):
    global login_button_clicked

    if not login_button_clicked:
        login_button_clicked = True
        mouse_click(login_screen_button.position)

        while True:
            upgrade_current_screen()
            metamask_login_button = detect_image_location('samples/metamask-login-button.png')

            if metamask_login_button.exist:
                mouse_click(metamask_login_button.position)
                break



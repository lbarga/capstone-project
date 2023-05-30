from detection import *
from mouse import *
from timer import *
from screen import *

in_heroes = False
in_character_section = False
tired = False


def in_heroes_screen():
    return detect_image_location('samples/heroes-upgrade-button.png')


def enter_in_heroes():
    global in_heroes
    heroes_button = detect_image_location('samples/heroes-button.png')

    if heroes_button.exist:
        in_heroes = True
        mouse_click(heroes_button.position)

def exit_heroes_screen():
    global in_heroes
    global tired
    global in_character_section

    heroes_close_button = detect_image_location('samples/heroes-close-button.png')

    if heroes_close_button.exist:
        in_heroes = False
        in_character_section = False
        tired = False
        mouse_click(heroes_close_button.position)

def set_characters_to_work():
    global in_character_section

    characters_flag = detect_image_location('samples/heroes-characters.png')

    if characters_flag.exist:
        mouse_move_and_click(characters_flag.position)
        in_character_section = True
        mouse_scroll()

        sleep(2)

        while True:
            upgrade_current_screen()
            
            disable_work_buttons = detect_all_image_location('samples/heroes-disable-work-button.png', 0.9)

            if disable_work_buttons.exist:
                total_work_buttons = len(disable_work_buttons.position)

                last_work_button = disable_work_buttons.position[total_work_buttons-1]

                heroes = 15

                while heroes:
                    mouse_click(last_work_button)
                    sleep(1)
                    heroes -= 1
                exit_heroes_screen()
                break




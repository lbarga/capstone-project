import time
from map import *
from screen import *

def sleep(input_seconds):
    time.sleep(input_seconds)

def countdown(input_seconds = 3600):
    while input_seconds:
        upgrade_current_screen()
        minutes, seconds = divmod(input_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        skip_new_map_modal()
        print('{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds))  # Python 3
        time.sleep(1)
        input_seconds -= 1
    print('rested')


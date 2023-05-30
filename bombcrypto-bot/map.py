from detection import *
from mouse import *



def skip_new_map_modal():

    new_map_button_modal = detect_image_location('samples/new-map-button-modal.png')

    if new_map_button_modal.exist:
        mouse_click(new_map_button_modal.position)

import pyautogui

def mouse_click(coordinates, x = 25, y = 25):
    position_x = coordinates[0] + x
    position_y = coordinates[1] + y
    pyautogui.click(position_x, position_y)

def mouse_move_and_click(coordinates):
    position_x = coordinates[0] + 100
    position_y = coordinates[1] + 100
    pyautogui.moveTo(position_x, position_y)
    mouse_click([position_x, position_y])

def mouse_scroll():
    pyautogui.scroll(-2000)

def mouse_dragTo(coordinates):
    position_x = coordinates[0]
    position_y = coordinates[1]
    pyautogui.dragTo(position_x + 18, position_y, 2, button='left')

def mouse_moveTo(coordinates, x = 10, y = 10):
    position_x = coordinates[0] + x
    position_y = coordinates[1] + y
    pyautogui.moveTo(position_x, position_y, 1)

def mouse_down():
    pyautogui.mouseDown()

def mouse_up():
    pyautogui.mouseUp()
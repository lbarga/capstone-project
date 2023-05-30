from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con,MOUSEEVENTF_LEFTUP,0,0)

while keyboard.is_pressed('q') == False:
    if (pyautogui.pixel(350, 590)[0]) == 0:
        click(350,590)
    if (pyautogui.pixel(450, 590)[0]) == 0:
        click(450,590)
    if (pyautogui.pixel(510, 590)[0]) == 0:
        click(510,590)
    if (pyautogui.pixel(580, 590)[0]) == 0:
        click(580,590)
        



# X:  687 Y:  543 RGB: (  0,   0,   0) #BLACK
# X:  368 Y:  593 RGB: (  0,   0,   0) #1
# X:  447 Y:  597 RGB: ( 77,  81, 115) #2
# X:  510 Y:  590 RGB: ( 89,  91, 117) #3
# X:  581 Y:  584 RGB: ( 85,  87, 116) #4

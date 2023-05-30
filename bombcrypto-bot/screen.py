import numpy as np
import cv2 as cv
import pyscreenshot as ImageGrab

def upgrade_current_screen():
    img = ImageGrab.grab()
    img_np = np.array(img)
    image = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
    cv.imwrite('samples/current-screen.jpg', image)

def get_current_screen():
    return cv.imread('samples/current-screen.jpg', cv.IMREAD_UNCHANGED)
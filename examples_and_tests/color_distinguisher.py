import cv2

import numpy as np


def distinguish(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    if avg_color[0] <= 40:
        return 3
    elif 50 <= avg_color[0] <= 80:
        return 2
    elif avg_color[0] >= 140:
        return 1

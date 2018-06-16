import cv2

import numpy as np

for i in range(1, 8):
    img = cv2.imread(f'crops/crop{i}.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    if avg_color[0] <= 40:
        print('Yellow')
    elif 50 <= avg_color[0] <= 80:
        print('Green')
    elif avg_color[0] >= 140:
        print('Pink')

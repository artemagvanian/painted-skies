import cv2

import numpy as np

universal_hsv_min = np.array((0, 20, 150), np.uint8)
universal_hsv_max = np.array((255, 255, 255), np.uint8)

crops = []

for i in range(1, 32):
    img = cv2.imread(f'strings/crop{i}.png')
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # применяем цветовой фильтр
    thresh = cv2.inRange(hsv, universal_hsv_min, universal_hsv_max)

    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Пересохраняем вырезанные области
    for j in contours:
        # Фильтруем по размеру
        if cv2.contourArea(j) > 2000:
            x, y, w, h = cv2.boundingRect(j)
            crop_img = img[y:y + h, x:x + w]
            crops.append(crop_img)

for n, i in enumerate(reversed(crops)):
    cv2.imwrite(f'crops/crop{n + 1}.png', i)

import cv2
from typing import List

import numpy as np
from numpy.core.multiarray import ndarray


class MultiColorProcessor():
    def get_crops_from_strings(self, strings: List[ndarray]) -> List[ndarray]:
        '''
        Обрабатывает строки и выделяет цветные кусочки
        '''
        universal_hsv_min = np.array((0, 20, 150), np.uint8)
        universal_hsv_max = np.array((255, 255, 255), np.uint8)

        crops = []

        for i in strings:
            # преобразуем BGR картинку в HSV модель
            hsv = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
            # применяем цветовой фильтр
            thresh = cv2.inRange(hsv, universal_hsv_min, universal_hsv_max)
            # выделяем контуры
            _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Пересохраняем вырезанные области
            for j in contours:
                # Фильтруем по размеру
                if cv2.contourArea(j) > 2000:
                    # выделяем прямоугольник из контура
                    x, y, w, h = cv2.boundingRect(j)
                    # вырезаем его
                    crop_img = i[y:y + h, x:x + w]
                    crops.append(crop_img)

        return list(reversed(crops))

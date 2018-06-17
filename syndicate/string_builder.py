import cv2

from numpy.core.multiarray import ndarray
from typing import List

from syndicate.kernel import Kernel


class StringBuilder():
    def to_strings(self, img: ndarray) -> List[ndarray]:
        '''
        Разбивает картинку текста на строчки
        '''
        # Значение этого параметра зависит от расстояния между словами в тексте
        N_HORIZONTAL_ITERATIONS = 30
        # Количество операций расширения выделения строки в направлении двух осей
        N_CROSS_ITERATIONS = 5
        # Размер ядра для свёртки и морф. операций
        KERNEL_SIZE = 5
        # Минимальный размер контура для выбора
        CONTOUR_MIN_AREA = 2000

        strings = []
        horizontal_kernel = Kernel.get_horizontal_kernel(KERNEL_SIZE)

        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processing_img = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        processing_img = cv2.bitwise_not(processing_img)
        processing_img = cv2.morphologyEx(processing_img, cv2.MORPH_OPEN,
                                          cv2.getStructuringElement(cv2.MORPH_RECT, (KERNEL_SIZE, KERNEL_SIZE)))
        processing_img = cv2.dilate(processing_img, horizontal_kernel, iterations=N_HORIZONTAL_ITERATIONS)
        processing_img = cv2.dilate(processing_img,
                                    cv2.getStructuringElement(cv2.MORPH_CROSS, (KERNEL_SIZE, KERNEL_SIZE)),
                                    iterations=N_CROSS_ITERATIONS)
        _, contours, _ = cv2.findContours(processing_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if cv2.contourArea(cnt) > CONTOUR_MIN_AREA:
                crop_img = img[y:y + h, x:x + w]
                strings.append(crop_img)

        return strings

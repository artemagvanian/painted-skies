import cv2
from typing import List

import pytesseract
from PIL import Image
from numpy.core.multiarray import ndarray

from syndicate.crop_info import CropInfo


class OCRApplier():
    def recognize(self, crop_infos: List[CropInfo]) -> List[CropInfo]:
        '''
        Возвращает текстовое представление отфильтрованного кусочка
        '''
        nodes = []

        for item in crop_infos:
            item.data = pytesseract.image_to_string(Image.fromarray(item.img), lang='eng')
            print(item.data)
            nodes.append(item)
        return nodes

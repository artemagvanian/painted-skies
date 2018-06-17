import cv2
from typing import List

import numpy as np
from numpy.core.multiarray import ndarray

from syndicate.crop_info import CropInfo
from syndicate.markup import Markup


class ColorDistinguisher():
    def distinguish(self, crops: List[ndarray], markup: Markup = None) -> List[CropInfo]:
        '''
        Опеределяет цвет кусочка и соответственно уровень
        '''
        crop_infos = []
        for img in crops:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            avg_color_per_row = np.average(img, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            if avg_color[0] <= 40:
                level = 3
            elif 50 <= avg_color[0] <= 80:
                level = 2
            elif avg_color[0] >= 140:
                level = 1
            else:
                level = -1
            if level != -1:
                info = CropInfo()
                info.level = level
                info.img = img
                crop_infos.append(info)
        return crop_infos

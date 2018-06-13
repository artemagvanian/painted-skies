from typing import List

from numpy.core.multiarray import ndarray

from syndicate.crop_info import CropInfo


class MultiColorProcessor():
    def get_crops_from_strings(self, strings: List[ndarray]) -> List[CropInfo]:
        '''
        Обрабатывает строки и выделяет цветные кусочки
        '''
        pass
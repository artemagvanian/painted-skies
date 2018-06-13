from numpy.core.multiarray import ndarray

from syndicate.crop_info import CropInfo
from syndicate.markup import Markup


class ColorDistinguisher():
    def distinguish(self, img: ndarray, markup: Markup) -> CropInfo:
        '''
        Опеределяет цвет кусочка и соответственно уровень
        '''
        pass
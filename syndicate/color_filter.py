from numpy.core.multiarray import ndarray

from syndicate.filter import Filter


class ColorFilter():
    def filter(self, img: ndarray, filter: Filter) -> ndarray:
        '''
        Фильтрует изображение для улучшения распознаваемости движком OCR
        '''
        pass
from numpy.core.multiarray import ndarray


class CropInfo():
    '''
    Вспомагательный класс для хранения информации о кусочке
    '''
    img: ndarray
    level: int
    data: str

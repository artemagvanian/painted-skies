import numpy as np


class Kernel():
    '''
    Вспомагательный класс дял получения ядер для морф. операций нужного размера
    '''

    @staticmethod
    def get_horizontal_kernel(size):
        kernel = np.zeros((size, size), dtype=np.uint8)
        if size % 2 == 1:
            kernel[size // 2] = np.ones(size)
        else:
            kernel[size // 2] = np.ones(size)
            kernel[size // 2 - 1] = np.ones(size)
        return kernel

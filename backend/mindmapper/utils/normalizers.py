from abc import ABC, abstractmethod
from pymorphy2 import MorphAnalyzer


class AbstractNormalizer(ABC):
    @abstractmethod
    def normalize(self, data):
        pass


class PyMorphyNormalizer(AbstractNormalizer):
    def __init__(self):
        self.morph = MorphAnalyzer()

    def normalize(self, data):
        data = [self.morph.parse(i)[0].normal_form for i in data.split()]
        return ' '.join(data)

from abc import ABC, abstractmethod

from fuzzywuzzy import fuzz

from .normalizers import PyMorphyNormalizer


class AbstractNodeComparator(ABC):
    def __init__(self, a, b, threshold):
        self.a = a
        self.b = b
        self.threshold = threshold

    @abstractmethod
    def compare(self):
        pass


class NormalizedLevenshteinNodeComparator(AbstractNodeComparator):
    def compare(self):
        normalizer = PyMorphyNormalizer()
        a, b = normalizer.normalize(self.a), normalizer.normalize(self.b)
        return fuzz.token_set_ratio(a, b) >= self.threshold

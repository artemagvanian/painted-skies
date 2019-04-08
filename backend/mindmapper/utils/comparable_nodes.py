from abc import ABC, abstractmethod

from .node_comparators import NormalizedLevenshteinNodeComparator


class AbstractComparableNode(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def __eq__(self, other):
        pass


class NormalizedLevenshteinComparableNode(AbstractComparableNode):
    def __repr__(self):
        return f"NormalizedLevenshteinComparableNode({self.data})"

    def __eq__(self, other):
        cmp = NormalizedLevenshteinNodeComparator(self.data, other.data, .5)
        return cmp.compare()

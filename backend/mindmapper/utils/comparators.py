from abc import ABC, abstractmethod
import json


class AbstractComparator(ABC):
    # compare a with b, assuming b is 100%
    def __init__(self, a, b, normalizer):
        self.a = json.loads(a)
        self.b = json.loads(b)
        self.normalizer = normalizer

    @abstractmethod
    def compare(self):
        pass

    @abstractmethod
    def apply_normalizer(self):
        pass


class NodeConnectionComparator(AbstractComparator):
    def apply_normalizer(self):
        for i in self.a['nodes']:
            i['label'] = self.normalizer.normalize(i['label'])

        for i in self.b['nodes']:
            i['label'] = self.normalizer.normalize(i['label'])

    def compare_nodes(self):
        nodes_a = [i['label'] for i in self.a['nodes']]
        nodes_b = [i['label'] for i in self.b['nodes']]

        intersection = list(set(nodes_a) & set(nodes_b))

        nodes_score = len(intersection) / len(nodes_b)

        return nodes_score

    def compare_edges(self):
        def get_label_by_id(nodes, node_id):
            for i in nodes:
                if i['id'] == node_id:
                    return i['label']

        nodes_a = self.a['nodes']
        nodes_b = self.b['nodes']

        edges_a = [frozenset({'from': get_label_by_id(nodes_a, i['from']),
                              'to': get_label_by_id(nodes_a, i['to'])}.items()) for i in self.a['edges']]

        edges_b = [frozenset({'from': get_label_by_id(nodes_b, i['from']),
                              'to': get_label_by_id(nodes_b, i['to'])}.items()) for i in self.b['edges']]

        intersection = list(set(edges_a) & set(edges_b))

        edges_score = len(intersection) / len(edges_b)

        return edges_score

    def compare(self):
        self.apply_normalizer()
        return self.compare_nodes() + self.compare_edges()

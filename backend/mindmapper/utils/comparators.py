import json
from abc import ABC, abstractmethod

import networkx as nx


class AbstractComparator(ABC):
    # compare a with b, assuming b is 100%
    def __init__(self, a, b, normalizer):
        self.normalizer = normalizer

        def load_graph(json_graph):
            data = json.loads(json_graph)
            graph = nx.Graph()

            for i in data['nodes']:
                node_id = i['id']
                del i['id']
                i['label'] = self.normalizer.normalize(i['label'])
                graph.add_node(node_id, **i)

            for i in data['edges']:
                if i['from'] in graph.nodes and i['to'] in graph.nodes:
                    graph.add_edge(i['from'], i['to'])

            return graph

        self.a, self.b = load_graph(a), load_graph(b)

    @abstractmethod
    def compare(self):
        pass


class DisjointComparator(AbstractComparator):
    @staticmethod
    def convert_edges_view(g):
        edges_id_list = list(g.edges)
        edges_labels_list = []
        for i in edges_id_list:
            label_from = g.nodes[i[0]]['label']
            label_to = g.nodes[i[1]]['label']
            edges_labels_list.append((label_from, label_to))
        return edges_labels_list

    def compare(self):
        edges_a, edges_b = set(self.convert_edges_view(self.a)), set(self.convert_edges_view(self.b))
        if len(edges_b) != 0:
            return int(len(edges_a & edges_b) / len(edges_b) * 100)
        else:
            return 0


def mock_test():
    from .normalizers import PyMorphyNormalizer as Nrm
    a = '{"nodes":[{"id":0,"label":"Генетический код"},{"id":1,"label":"совокупность правил"},{"id":2,"label":"которым"},{"id":3,"label":"информация переводится"}],"edges":[{"from":1,"to":0},{"from":2,"to":1},{"from":3,"to":2}]}'
    b = '{"nodes":[{"id":0,"label":"Генетические код"},{"id":1,"label":"совокупности правил"},{"id":2,"label":"которые"},{"id":3,"label":"информация переводится"}],"edges":[{"from":1,"to":0},{"from":2,"to":1},{"from":3,"to":2}]}'

    cmps = [DisjointComparator(a, b, Nrm())]

    print([i.compare() for i in cmps])

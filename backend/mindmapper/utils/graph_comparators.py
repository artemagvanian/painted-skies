import json
from abc import ABC, abstractmethod

import networkx as nx

from .comparable_nodes import NormalizedLevenshteinComparableNode


class AbstractGraphComparator(ABC):
    # compare a with b, assuming b is 100%
    def __init__(self, a, b):
        def load_graph(json_graph):
            data = json.loads(json_graph)
            graph = nx.Graph()

            for i in data['nodes']:
                node_id = i['id']
                del i['id']
                graph.add_node(node_id, **i)

            for i in data['edges']:
                if i['from'] in graph.nodes and i['to'] in graph.nodes:
                    graph.add_edge(i['from'], i['to'])

            return graph

        self.a, self.b = load_graph(a), load_graph(b)

    @abstractmethod
    def compare(self):
        pass


class EdgeGraphComparator(AbstractGraphComparator):
    @staticmethod
    def convert_edges(graph):
        edges_id_list = list(graph.edges)
        edges_labels_list = []
        for edge in edges_id_list:
            label_from, label_to = sorted([graph.nodes[edge[0]]['label'], graph.nodes[edge[1]]['label']])
            edges_labels_list.append(
                (NormalizedLevenshteinComparableNode(label_from), NormalizedLevenshteinComparableNode(label_to)))
        return edges_labels_list

    def compare(self):
        edges_a, edges_b = set(self.convert_edges(self.a)), set(self.convert_edges(self.b))
        if len(edges_b) != 0:
            return int(len(edges_a & edges_b) / len(edges_b) * 100)
        else:
            return 0


def mock_test():
    a = '{"nodes":[{"id":0,"label":"Генетический код"},{"id":1,"label":"совокупность правил"},{"id":2,"label":"которым"},{"id":3,"label":"информация переводится"}],"edges":[{"from":1,"to":0},{"from":2,"to":1},{"from":3,"to":2}]}'
    b = '{"nodes":[{"id":0,"label":"Генетические код"},{"id":1,"label":"совокупности правил"},{"id":2,"label":"которые"},{"id":3,"label":"информация переводится"}],"edges":[{"from":1,"to":0},{"from":2,"to":1},{"from":3,"to":2}]}'

    cmps = [EdgeGraphComparator(a, b)]

    print([i.compare() for i in cmps])

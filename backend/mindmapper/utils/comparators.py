from abc import ABC, abstractmethod
import json
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
                graph.add_edge(i['from'], i['to'])

            return graph

        self.a, self.b = load_graph(a), load_graph(b)

    @abstractmethod
    def compare(self):
        pass


class DisjointComparator(AbstractComparator):
    def compare(self):
        diff = nx.difference(self.b, self.a)
        print(nx.number_of_nodes(diff))
        return nx.number_of_edges(diff) / nx.number_of_edges(self.b) + \
               1 - nx.number_of_nodes(diff) / nx.number_of_nodes(self.b)


class NodeConnectionComparator(AbstractComparator):
    def compare_nodes(self):
        nodes_a = [i[1]['label'] for i in self.a.nodes(data=True)]
        nodes_b = [i[1]['label'] for i in self.b.nodes(data=True)]

        intersection = list(set(nodes_a) & set(nodes_b))

        nodes_score = len(intersection) / len(nodes_b)

        return nodes_score

    def compare_edges(self):
        def get_label_by_id(nodes, node_id):
            for i in nodes:
                if i[0] == node_id:
                    return i[1]['label']

        nodes_a = self.a.nodes(data=True)
        nodes_b = self.b.nodes(data=True)

        edges_a = [frozenset({'from': get_label_by_id(nodes_a, i[0]),
                              'to': get_label_by_id(nodes_a, i[1])}.items()) for i in self.a.edges]

        edges_b = [frozenset({'from': get_label_by_id(nodes_b, i[0]),
                              'to': get_label_by_id(nodes_b, i[1])}.items()) for i in self.b.edges]

        intersection = list(set(edges_a) & set(edges_b))

        edges_score = len(intersection) / len(edges_b)

        return edges_score

    def compare(self):
        return self.compare_nodes() + self.compare_edges()


def mock_test():
    from .normalizers import PyMorphyNormalizer as Nrm
    a = '{"nodes":[{"id":0,"label":"Генетический код"},{"id":1,"label":"совокупность правил"},{"id":2,"label":"которым"},{"id":3,"label":"информация переводится"}],"edges":[{"from":1,"to":0},{"from":2,"to":1},{"from":3,"to":2}]}'
    b = '{"nodes":[{"id":0,"label":"Генетические код"},{"id":1,"label":"совокупности правил"},{"id":2,"label":"которые"},{"id":3,"label":"информация переводится"}],"edges":[{"from":1,"to":0},{"from":2,"to":1},{"from":3,"to":2}]}'

    cmps = [DisjointComparator(a, b, Nrm()),
            NodeConnectionComparator(a, b, Nrm())]

    print([i.compare() for i in cmps])

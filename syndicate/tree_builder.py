from typing import List

from graphviz import Digraph

from syndicate.crop_info import CropInfo


class TreeBuilder():
    def build(self, nodes: List[CropInfo]):
        '''
        Строит визуальное дерево по данным уровням
        '''
        dot = Digraph(comment='Conspect')
        stack = []
        for n, i in enumerate(nodes):
            dot.node(str(n), i.data)
            if n == 0:
                stack.append(str(n))
            else:
                if i.level > nodes[n - 1].level:
                    dot.edge(str(n), stack[len(stack) - 1])
                    stack.append(str(n))
                elif i.level == nodes[n - 1].level:
                    stack.pop()
                    dot.edge(str(n), stack[len(stack) - 1])
                    stack.append(str(n))
                elif i.level < nodes[n - 1].level:
                    stack.pop()
                    stack.pop()
                    dot.edge(str(n), stack[len(stack) - 1])
                    stack.append(str(n))

        dot.render('test-output/round-table.gv', view=True)

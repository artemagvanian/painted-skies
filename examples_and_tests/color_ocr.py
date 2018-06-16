import cv2
import numpy as np
import pytesseract
from PIL import Image

from graphviz import Digraph


def distinguish(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    if avg_color[0] <= 40:
        return 3
    elif 50 <= avg_color[0] <= 80:
        return 2
    elif avg_color[0] >= 140:
        return 1


nodes = []

for i in range(1, 8):
    img = cv2.imread(f'crops/crop{i}.png')
    resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # cv2.imshow('img', resized)
    # cv2.waitKey(0)
    nodes.append({
        'data': pytesseract.image_to_string(Image.fromarray(resized), lang='eng'),
        'level': distinguish(img)
    })

dot = Digraph(comment='Conspect')
stack = []
for n, i in enumerate(nodes):
    dot.node(str(n), i['data'])
    if n == 0:
        stack.append(str(n))
    else:
        if i['level'] > nodes[n - 1]['level']:
            dot.edge(str(n), stack[len(stack) - 1])
            stack.append(str(n))
        elif i['level'] == nodes[n - 1]['level']:
            stack.pop()
            dot.edge(str(n), stack[len(stack) - 1])
            stack.append(str(n))
        elif i['level'] < nodes[n - 1]['level']:
            stack.pop()
            stack.pop()
            dot.edge(str(n), stack[len(stack) - 1])
            stack.append(str(n))


dot.render('test-output/round-table.gv', view=True)

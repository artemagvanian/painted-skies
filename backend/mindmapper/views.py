import os

from django.http import JsonResponse
from django.views import View
import json

import base64

import io
from PIL import Image

import pytesseract

import subprocess
import uuid


class ProcessView(View):
    def process_canvas(self, canvas):
        image = \
            Image.open(
                io.BytesIO(
                    base64.b64decode(
                        canvas['backgroundImage']['src'].split(",")[1])))

        image = image.resize((int(image.width * canvas['backgroundImage']['scaleX']),
                              int(image.height * canvas['backgroundImage']['scaleY'])))

        image_name = str(uuid.uuid4())

        image.save(image_name + '.png', format="PNG")
        subprocess.call(['./textcleaner.sh', image_name + '.png', image_name + 'cleaned.png'])
        image = Image.open(image_name + 'cleaned.png')
        os.remove(image_name + '.png')
        os.remove(image_name + 'cleaned.png')

        rectangles = list(map(lambda x: {
            'left': x['left'],
            'top': x['top'],
            'width': x['width'],
            'height': x['height'],
            'fill': x['fill']

        }, canvas['objects']))
        return image, rectangles

    def post(self, request):
        canvas = json.loads(request.POST['canvas'])
        lang = request.POST['lang']
        print('[TESSERACT]: obtained data')
        image, rectangles = self.process_canvas(canvas)
        print('[TESSERACT]: obtained image')
        color_to_level = {
            'rgba(255,0,0,.5)': 1,
            'rgba(0,255,0,.5)': 2,
            'rgba(0,0,255,.5)': 3
        }

        color_to_shape = {
            'rgba(255,0,0,.5)': 'ellipse',
            'rgba(0,255,0,.5)': 'box',
            'rgba(0,0,255,.5)': 'box'
        }

        color_to_text = {
            'rgba(255,0,0,.5)': 'white',
            'rgba(0,255,0,.5)': 'black',
            'rgba(0,0,255,.5)': 'white'
        }

        regions = list(
            map(lambda x: {
                'image': image.crop((
                    x['left'],
                    x['top'],
                    x['left'] + x['width'],
                    x['top'] + x['height'])),
                'level': color_to_level[x['fill']],
                'color': x['fill']
            }, rectangles))

        print('[TESSERACT]: obtained crops')

        nodes = []
        edges = []
        stack = []

        print(f'[TESSERACT]: going to recognize {len(regions)} crops')

        for n, i in enumerate(regions):

            if i['image'].width == 0 or i['image'].height == 0:
                nodes.append({
                    'id': n,
                    'label': '',
                    'color': i['color'][:13] + '1)',
                    'shape': color_to_shape[i['color']],
                    'font': {'color': color_to_text[i['color']]}
                })
            else:
                nodes.append({
                    'id': n,
                    'label': pytesseract.image_to_string(i['image'], lang=lang),
                    'color': i['color'][:13] + '1)',
                    'shape': color_to_shape[i['color']],
                    'font': {'color': color_to_text[i['color']]}
                })

            if n == 0:
                stack.append(n)
            else:
                if i['level'] - regions[stack[-1]]['level'] == 1:
                    # dot.edge(n, stack[len(stack) - 1])
                    edges.append({
                        'from': n,
                        'to': stack[-1],
                        'arrows': 'from'
                    })
                    stack.append(n)
                elif i['level'] == regions[stack[-1]]['level']:
                    stack.pop()
                    # dot.edge(n, stack[len(stack) - 1])
                    edges.append({
                        'from': n,
                        'to': stack[-1],
                        'arrows': 'from'
                    })
                    stack.append(n)
                elif i['level'] - regions[stack[-1]]['level'] == -1:
                    stack.pop()
                    stack.pop()
                    # dot.edge(n, stack[len(stack) - 1])
                    edges.append({
                        'from': n,
                        'to': stack[-1],
                        'arrows': 'from'
                    })
                    stack.append(n)

            print(f'[TESSERACT]: recognized crop {n}')

        print('[TESSERACT]: obtained mindmap')

        return JsonResponse({
            'edges': edges,
            'nodes': nodes,
            'status': 'ok'
        })

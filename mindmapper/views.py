from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import json

import base64

import io
from PIL import Image

from django.views.decorators.csrf import csrf_exempt
import pytesseract


@method_decorator(csrf_exempt, name='dispatch')
class ProcessView(View):
    def process_canvas(self, canvas):
        image = \
            Image.open(
                io.BytesIO(
                    base64.b64decode(
                        canvas['backgroundImage']['src'].split(",")[1])))

        image = image.resize((int(image.width * canvas['backgroundImage']['scaleX']),
                              int(image.height * canvas['backgroundImage']['scaleY'])))

        rectangles = list(map(lambda x: {
            'left': x['left'],
            'top': x['top'],
            'width': x['width'],
            'height': x['height'],
            'fill': x['fill']

        }, canvas['objects']))
        return image, rectangles

    def post(self, request):
        print(request.POST)
        canvas = json.loads(request.POST['canvas'])
        lang = request.POST['lang']
        image, rectangles = self.process_canvas(canvas)

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

        nodes = []
        edges = []
        stack = []

        for n, i in enumerate(regions):
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

        return JsonResponse({
            'edges': edges,
            'nodes': nodes,
            'status': 'ok'
        })

from django.http import HttpResponse, JsonResponse
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
        canvas = json.loads(request.POST['canvas'])
        image, rectangles = self.process_canvas(canvas)

        color_to_level = {
            'rgba(255,0,0,.5)': 1,
            'rgba(0,255,0,.5)': 2,
            'rgba(0,0,255,.5)': 3
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
            # if i['level'] == 1:
            #     color = 'red'
            # elif i['level'] == 2:
            #     color = 'green'
            # else:
            #     color = 'blue'
            # dot.node(str(n), i.data, color=color, style='filled')
            nodes.append({
                'id': n,
                'label': pytesseract.image_to_string(i['image'], lang='eng'),
                'color': i['color']
            })

            if n == 0:
                stack.append(n)
            else:
                if i['level'] > regions[n - 1]['level']:
                    # dot.edge(n, stack[len(stack) - 1])
                    edges.append({
                        'from': n,
                        'to': stack[len(stack) - 1]
                    })
                    stack.append(n)
                elif i['level'] == regions[n - 1]['level']:
                    stack.pop()
                    # dot.edge(n, stack[len(stack) - 1])
                    edges.append({
                        'from': n,
                        'to': stack[len(stack) - 1]
                    })
                    stack.append(n)
                elif i['level'] < regions[n - 1]['level']:
                    stack.pop()
                    stack.pop()
                    # dot.edge(n, stack[len(stack) - 1])
                    edges.append({
                        'from': n,
                        'to': stack[len(stack) - 1]
                    })
                    stack.append(n)

        return JsonResponse({
            'edges': edges,
            'nodes': nodes
        })

import PIL
import os

import numpy as np
from django.http import JsonResponse, HttpResponse

from django.views import View
import json

import base64

import io
from PIL import Image

import pytesseract

import subprocess
import uuid


from pdf2image import convert_from_bytes


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


class PdfMergeView(View):
    def post(self, request):
        try:
            first_page, last_page = int(request.POST['first']), int(request.POST['last'])
            pdf = request.FILES['pdf']
        except KeyError:
            return HttpResponse(status=400)

        if last_page - first_page > 10 or last_page - first_page < 0 or first_page <= 0 or last_page <= 0:
            return HttpResponse(status=400)

        pages = convert_from_bytes(pdf.file.read(), first_page=first_page, last_page=last_page)
        min_shape = sorted([(np.sum(i.size), i.size) for i in pages])[0][1]
        page_vstack = np.vstack((np.asarray(i.resize(min_shape)) for i in pages))
        page_vstack = PIL.Image.fromarray(page_vstack)

        buffered = io.BytesIO()
        page_vstack.save(buffered, format="png")
        img_str = b"data:image/png;base64," + base64.b64encode(buffered.getvalue())

        response = HttpResponse(img_str)

        return response

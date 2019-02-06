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

from django.middleware.csrf import get_token

from pdf2image import convert_from_bytes


class ProcessView(View):
    def process_image(self, image, scale):
        image = \
            Image.open(
                io.BytesIO(
                    base64.b64decode(
                        image.split(",")[1])))

        image = image.resize((int(image.width * scale),
                              int(image.height * scale)))

        image_name = str(uuid.uuid4())

        image.save(image_name + '.png', format="PNG")
        subprocess.call(['./textcleaner.sh', image_name + '.png', image_name + 'cleaned.png'])
        image = Image.open(image_name + 'cleaned.png')
        os.remove(image_name + '.png')
        os.remove(image_name + 'cleaned.png')

        return image

    def post(self, request):
        rectangles = json.loads(request.POST['selections'])
        lang = request.POST['lang']
        image = self.process_image(request.POST['image'], float(request.POST['scale']))
        print('[TESSERACT]: obtained data')

        print('[TESSERACT]: obtained image')

        regions = []
        for num, data in enumerate(rectangles):
            x1 = min(data['x'], data['x'] + data['width'])
            y1 = min(data['y'], data['y'] + data['height'])
            x2 = max(data['x'], data['x'] + data['width'])
            y2 = max(data['y'], data['y'] + data['height'])

            regions.append({
                'image': image.crop((x1, y1, x2, y2)),
                'level': data['level'],
                'color': data['color']['stroke'],
                'id': num,
                'merged': data['merged']
            })

        print('[TESSERACT]: obtained crops')

        nodes = []
        edges = []

        print(f'[TESSERACT]: going to recognize {len(regions)} crops')

        for i in regions:
            if not i['merged']:
                nodes.append({
                    'id': i['id'],
                    'label': pytesseract.image_to_string(i['image'], lang=lang),
                    'color': i['color'],
                    'shape': 'box',
                    'font': {'color': 'white'}
                })

                for j in reversed(regions[:i['id']]):
                    if i['level'] - j['level'] == 1 and not j['merged']:
                        edges.append({
                            'from': i['id'],
                            'to': j['id'],
                            'arrows': 'from'
                        })
                        break
            else:
                nodes[-1]['label'] += ' ' + pytesseract.image_to_string(i['image'], lang=lang)

            print(f'[TESSERACT]: recognized crop {i["id"]}')

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

        if last_page - first_page > 20 or last_page - first_page < 0 or first_page <= 0 or last_page <= 0:
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


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'token': token})

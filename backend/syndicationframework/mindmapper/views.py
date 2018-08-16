from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
import json

import base64

import io
from PIL import Image

from django.views.decorators.csrf import csrf_exempt


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

        regions = list(
            map(lambda x: image.crop((
                x['left'],
                x['top'],
                x['left'] + x['width'],
                x['top'] + x['height'])), rectangles))

        for n, d in enumerate(regions):
            d.save(f'{n}.png')

        return HttpResponse(status=200)

import base64
import io
import json

import pytesseract
from PIL import Image
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class ProcessView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def process_image(image, scale):
        image = \
            Image.open(
                io.BytesIO(
                    base64.b64decode(
                        image.split(",")[1])))

        image = image.resize((int(image.width * scale),
                              int(image.height * scale)))

        # image_name = str(uuid.uuid4())

        # image.save(image_name + '.png', format="PNG")
        # subprocess.call(['./textcleaner.sh', image_name + '.png', image_name + 'cleaned.png'])
        # image = Image.open(image_name + 'cleaned.png')
        # os.remove(image_name + '.png')
        # os.remove(image_name + 'cleaned.png')

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

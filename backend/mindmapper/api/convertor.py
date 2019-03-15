import base64
import io

import PIL
import numpy as np
from PIL import Image
from django.http import HttpResponse
from pdf2image import convert_from_bytes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class PdfMergeView(APIView):
    permission_classes = (AllowAny,)

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

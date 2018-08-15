from django.http import JsonResponse
from django.views import View


class ProcessView(View):
    def post(self, request):
        try:
            image = request.FILES['image']
            canvas = request.POST['canvas']
        except Exception:
            return JsonResponse({'error': "you haven't provided necessary data"})

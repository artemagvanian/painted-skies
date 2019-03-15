from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'token': token})


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)

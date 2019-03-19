from django.contrib.auth.forms import UserCreationForm
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class Signup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            form.save()
            return Response(status=201)
        return Response(form.errors, status=400)

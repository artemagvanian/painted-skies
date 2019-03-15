from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..serializers import UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(profile__classrooms__teacher_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

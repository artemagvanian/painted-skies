from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Classroom
from ..serializers import ClassroomSerializer


class ClassroomList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassroomSerializer

    def get_queryset(self):
        return Classroom.objects.filter(teacher=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ClassroomDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassroomSerializer

    def get_queryset(self):
        return Classroom.objects.filter(teacher=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

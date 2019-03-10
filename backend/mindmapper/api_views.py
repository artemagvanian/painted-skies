from datetime import datetime

from rest_framework.permissions import IsAuthenticated

from .models import Mindmap, Classroom
from .serializers import MindmapSerializer, ClassroomSerializer

from rest_framework import generics

from django.contrib.auth.models import User


class ClassroomList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassroomSerializer

    def get_queryset(self):
        return Classroom.objects.filter(teacher=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MindmapList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MindmapSerializer

    def get_queryset(self):
        return Mindmap.objects.filter(owner=self.request.user.id).order_by('-edited_at')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=User.objects.get(id=self.request.user.id),
                        created_at=datetime.now(),
                        edited_at=datetime.now())

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MindmapDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MindmapSerializer

    def get_queryset(self):
        return Mindmap.objects.filter(owner=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(edited_at=datetime.now())

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

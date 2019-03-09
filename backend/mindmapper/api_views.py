from datetime import datetime

from .models import Mindmap
from .serializers import MindmapSerializer

from rest_framework import generics


class MindmapList(generics.ListCreateAPIView):
    serializer_class = MindmapSerializer

    def get_queryset(self):
        return Mindmap.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, created_at=datetime.now())

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MindmapDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MindmapSerializer

    def get_queryset(self):
        return Mindmap.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

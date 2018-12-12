from datetime import datetime

from rest_framework import viewsets, permissions

from .models import Mindmap
from .serializers import MindmapSerializer


class MindmapViewSet(viewsets.ModelViewSet):
    queryset = Mindmap.objects.all()
    serializer_class = MindmapSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Mindmap.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, created_at=datetime.now())

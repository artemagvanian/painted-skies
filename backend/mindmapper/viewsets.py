from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .models import Mindmap
from .serializers import MindmapSerializer, UserSerializer


class MindmapViewSet(viewsets.ModelViewSet):
    queryset = Mindmap.objects.all()
    serializer_class = MindmapSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Mindmap.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, created_at=datetime.now())


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

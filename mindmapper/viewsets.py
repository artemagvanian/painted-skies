from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from mindmapper.models import Mindmap
from mindmapper.serializers import MindmapSerializer, UserSerializer


class MindmapViewSet(viewsets.ModelViewSet):
    queryset = Mindmap.objects.all()
    serializer_class = MindmapSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

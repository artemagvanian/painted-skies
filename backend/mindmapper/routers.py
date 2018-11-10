from rest_framework.routers import DefaultRouter
from . import viewsets

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('mindmaps', viewsets.MindmapViewSet)
router.register('users', viewsets.UserViewSet)

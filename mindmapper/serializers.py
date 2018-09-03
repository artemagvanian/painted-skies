from rest_framework import serializers

from mindmapper.models import Mindmap

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    mindmaps = serializers.PrimaryKeyRelatedField(many=True, queryset=Mindmap.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'mindmaps')


class MindmapSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Mindmap
        fields = ('id', 'title', 'mindmap', 'owner', 'created_at')

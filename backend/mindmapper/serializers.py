from rest_framework import serializers

from .models import Mindmap


class MindmapSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Mindmap
        fields = ('id', 'title', 'mindmap', 'owner', 'created_at')
        read_only_fields = ('owner', 'created_at')

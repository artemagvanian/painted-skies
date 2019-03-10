from rest_framework import serializers

from .models import Mindmap, Classroom


class MindmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mindmap
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'edited_at')


class ClassroomSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ('title', 'teacher', 'students')
        read_only_fields = ('teacher', 'students')

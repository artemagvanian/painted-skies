from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Mindmap, Classroom, Profile


class MindmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mindmap
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'edited_at')


class UserSerializer(serializers.ModelSerializer):
    mindmaps = MindmapSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'mindmaps')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user',)


class ClassroomSerializer(serializers.ModelSerializer):
    students = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ('id', 'title', 'teacher', 'students')
        read_only_fields = ('id', 'teacher', 'students')

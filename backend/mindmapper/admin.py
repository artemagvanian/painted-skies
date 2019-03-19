from django.contrib import admin

from .models import Mindmap, Classroom


class MindmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    list_filter = ('owner',)
    search_fields = ('title',)


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Mindmap, MindmapAdmin)
admin.site.register(Classroom, ClassroomAdmin)

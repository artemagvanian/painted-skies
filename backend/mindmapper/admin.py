from django.contrib import admin

from .models import Mindmap


class MindmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    list_filter = ('owner',)
    search_fields = ('title',)


admin.site.register(Mindmap, MindmapAdmin)

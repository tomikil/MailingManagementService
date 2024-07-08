from django.contrib import admin

from blogs.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'preview', 'country', )
    search_fields = ('title', )
    list_filter = ('created_at', )

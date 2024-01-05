from django.contrib import admin
from .models import Tags


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name')
    list_display_links = ('id', 'Name')
    search_fields = ('Name', 'id')


admin.site.register(Tags, TagsAdmin)


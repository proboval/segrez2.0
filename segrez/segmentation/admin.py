from django.contrib import admin
from .models import *


# это всё убрать из админки
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name')
    list_display_links = ('id', 'Name')
    search_fields = ('Name', 'id')


class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'x', 'x')
    list_display_links = ('id',)
    search_fields = ('id',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name')
    list_display_links = ('id', 'Name')
    search_fields = ('id', 'Name')


class RectAdmin(admin.ModelAdmin):
    list_display = ('id', 'inImage', 'tag')
    list_display_links = ('id', 'tag')
    search_fields = ('id',)


admin.site.register(Tags, TagsAdmin)
admin.site.register(Point, PointAdmin)
admin.site.register(segmentImage, ImageAdmin)
admin.site.register(Rect, RectAdmin)



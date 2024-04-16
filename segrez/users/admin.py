from django.contrib import admin
from .models import *


class ExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('id', 'first_name', 'last_name')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


admin.site.register(Expert, ExpertAdmin)
admin.site.register(Company, CompanyAdmin)

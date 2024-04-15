from django.contrib import admin
from .models import *


class ExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name', 'lastName')
    list_display_links = ('id', 'Name', 'lastName')
    search_fields = ('id', 'Name', 'lastName')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'companyName')
    list_display_links = ('id', 'companyName')
    search_fields = ('id', 'companyName')


admin.site.register(Expert, ExpertAdmin)
admin.site.register(Company, CompanyAdmin)

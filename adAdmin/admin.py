from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import CompanyInfo

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'state', 'zipcode')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:50px;"/>', obj.logo.url)
        return "-"
    logo_preview.short_description = 'Logo'


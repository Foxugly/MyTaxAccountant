from django.contrib import admin
from documents.models import Document, Page

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    filter_horizontal = ('pages',)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass
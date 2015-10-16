from django.contrib import admin
from trimesters.models import Trimester

@admin.register(Trimester)
class TrimesterAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)


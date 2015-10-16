from django.contrib import admin
from years.models import Year

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    filter_horizontal = ('trimesters',)


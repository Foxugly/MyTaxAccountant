from django.contrib import admin
from utils.models import Country, FiscalYear

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    pass


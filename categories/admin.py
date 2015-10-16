from django.contrib import admin
from categories.models import Category, TypeCategory


@admin.register(TypeCategory)
class TypeCategoryAdmin(admin.ModelAdmin):
	pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	filter_horizontal = ('documents',)


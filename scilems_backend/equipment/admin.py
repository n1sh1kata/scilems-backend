from django.contrib import admin
from .models import Category, Equipment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoryname')
    search_fields = ('categoryname',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'eqname', 'category', 'stock')
    list_filter = ('category',)
    search_fields = ('eqname', 'category__categoryname')
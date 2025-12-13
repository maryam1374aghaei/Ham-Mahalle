from django.contrib import admin
from .models import Category, Ad, AdImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'price', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']

    admin.site.register(AdImage)
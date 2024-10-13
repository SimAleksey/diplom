from django.contrib import admin
from .models import Category, Product, Comment, Color, Storage
# Register your models here.


class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'color', 'product_parent', 'price', 'shopping', 'preview']
    list_display_links = ['id', 'color']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    list_display_links = ['title', 'id']
    prepopulated_fields = {'slug': ('title',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'shopping', 'quantity', 'category', 'producer', 'price', 'color']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['shopping']
    list_editable = ['category', 'producer']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'author']
    list_filter = ['product']


class StorageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'product_color']
    list_display_links = ['id']


admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Storage, StorageAdmin)

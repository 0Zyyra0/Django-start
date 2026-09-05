from django.contrib import admin

from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'status', 'counted_view')
    list_filter = ('published_date', 'status', 'category')
    search_fields = ('title', 'content')
    list_editable = ('status',)

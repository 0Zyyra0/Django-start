from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'status', 'counted_view')
    list_filter = ('published_date', 'status')
    search_fields = ('title', 'content')
    list_editable = ('status',)

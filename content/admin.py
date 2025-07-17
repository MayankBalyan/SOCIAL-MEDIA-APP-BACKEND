from django.contrib import admin

from content.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'caption', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Content"
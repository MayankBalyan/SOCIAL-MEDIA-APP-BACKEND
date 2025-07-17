from django.contrib import admin
from interaction.models import Hashtag, PostComment


# Register your models here.
@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'post_count')
    search_fields = ('name',)
    ordering = ('-created_at',)

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Post Count'
admin.site.register(PostComment,)
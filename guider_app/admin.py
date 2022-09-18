from django.contrib import admin
from .models import Guide, Comment


class GuideAdmin(admin.ModelAdmin):
    fields = ['id', 'slug', 'title', 'text', 'moderated', 'updated_at', 'creator', 'image', 'likes', 'dislikes']
    readonly_fields = ['id', 'slug']
    pass


class CommentAdmin(admin.ModelAdmin):
    fields = ['id', 'guide', 'text', 'author', 'created_date']
    readonly_fields = ['id', 'created_date']


admin.site.register(Guide, GuideAdmin)
admin.site.register(Comment, CommentAdmin)

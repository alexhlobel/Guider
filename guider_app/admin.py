from django.contrib import admin
from .models import Guide, Comment
from django.utils.safestring import mark_safe


class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'creator', 'preview_image', 'total_likes', 'total_dislikes')
    fields = ['id', 'slug', 'title', 'text', 'moderated', 'updated_at', 'creator', 'image', 'likes', 'dislikes']
    readonly_fields = ['id', 'slug']

    @staticmethod
    def preview_image(obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return mark_safe('<img src="/static/img/no_image.png" width="100"/>')


class CommentAdmin(admin.ModelAdmin):
    fields = ['id', 'guide', 'text', 'author', 'created_date']
    readonly_fields = ['id', 'created_date']


admin.site.register(Guide, GuideAdmin)
admin.site.register(Comment, CommentAdmin)

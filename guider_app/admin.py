from django.contrib import admin
from .models import Guide


class GuideAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'slug': ('title',)}
    fields = ['id', 'slug', 'title', 'text', 'moderated', 'updated_at', 'creator', 'image']
    readonly_fields = ['id', 'slug']
    pass


admin.site.register(Guide, GuideAdmin)

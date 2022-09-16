from django.contrib import admin
from .models import Guide


class GuideAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Guide, GuideAdmin)

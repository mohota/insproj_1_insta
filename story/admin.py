from django.contrib import admin
from .models import StoryModel

@admin.register(StoryModel)
class ActionAdmin(admin.ModelAdmin):
	list_display = ('owner', 'image', 'created')


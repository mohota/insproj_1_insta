from django.contrib import admin
from django.contrib.auth.models import Group
from .models import UserProf, Contact, Re_quest, Blocking, Direct

admin.site.register(UserProf)
admin.site.register(Contact)
admin.site.register(Re_quest)
admin.site.register(Blocking)
admin.site.unregister(Group)


@admin.register(Direct)
class ActionAdmin(admin.ModelAdmin):
	list_display = ('user_from', 'user_to', 'show')
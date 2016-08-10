from django.contrib import admin

from carr.activity_taking_action.models import ActivityState


class ActivityStateAdmin(admin.ModelAdmin):
    list_display = ['user', 'json']
    search_fields = ['user__username']

admin.site.register(ActivityState, ActivityStateAdmin)

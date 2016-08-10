from django.contrib import admin

from carr.activity_bruise_recon.models import Case, ActivityState


class ActivityStateAdmin(admin.ModelAdmin):
    list_display = ['user', 'json']
    search_fields = ['user__username']

admin.site.register(ActivityState, ActivityStateAdmin)
admin.site.register(Case)

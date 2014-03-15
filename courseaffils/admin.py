from courseaffils.forms import CourseAdminForm
from courseaffils.models import Course, CourseSettings
from django.contrib import admin


class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSettings)

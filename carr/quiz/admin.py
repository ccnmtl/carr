from django.contrib import admin

from carr.quiz.models import ActivityState
from models import Quiz, Question, Answer


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['value', 'question']
    list_display = ('value', 'question')


class AnswerInline (admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['value']
    list_display = ['text', 'quiz', 'ordinality']
    inlines = [AnswerInline]


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)


class ActivityStateAdmin(admin.ModelAdmin):
    list_display = ['user', 'submitted', 'json']
    search_fields = ['user__username']


admin.site.register(ActivityState, ActivityStateAdmin)

from models import Quiz, Question, Answer

from django.contrib import admin


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

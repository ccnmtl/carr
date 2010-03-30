from models import Quiz, Question, Answer, Response

from django.contrib import admin


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['value', 'question']
    #search_fields = ['short_title', 'long_title', 'crib_notes']
    list_display = ('value', 'question')
    
    #list_display = ('short_title',  'long_title', 'id', 'clientsession', 'created', 'modified')
    #inlines = [InstructionInline]


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['value']
    #list_display = ('value', 'question')
    #list_display = ['text', 'quiz']
    list_display = ['text', 'ordinality']
    
    #list_display = ('short_title',  'long_title', 'id', 'clientsession', 'created', 'modified')
    #inlines = [InstructionInline]


admin.site.register(Quiz)


admin.site.register(Question, QuestionAdmin)


#admin.site.register(Answer)
admin.site.register(Answer, AnswerAdmin)

# we're not using responses in this site.
#admin.site.register(Response)


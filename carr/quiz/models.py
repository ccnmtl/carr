from django.db import models
from pagetree.models import PageBlock
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django import forms
from django.utils import timezone
from django.urls.base import reverse
from django.utils.encoding import smart_str


class Quiz(models.Model):
    pageblocks = GenericRelation(PageBlock)
    description = models.TextField(blank=True)
    rhetorical = models.BooleanField(default=False)
    template_file = "quiz/quizblock.html"
    js_template_file = "quiz/quizblock_js.html"

    display_name = "Quiz"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return smart_str(self.pageblock())

    def label(self):
        return self.pageblock().label

    def needs_submit(self):
        return not self.rhetorical

    def submit(self, user, data):
        """ a big open question here is whether we should
        be validating submitted answers here, on submission,
        or let them submit whatever garbage they want and only
        worry about it when we show the admins the results """
        s = Submission.objects.create(quiz=self, user=user)
        for k in data.keys():
            if k.startswith('question'):
                qid = int(k[len('question'):])
                question = Question.objects.get(id=qid)
                Response.objects.create(
                    submission=s,
                    question=question,
                    value=data[k])

    def unlocked(self, user):
        # meaning that the user can proceed *past* this one,
        # not that they can access this one. careful.
        # we're not keeping Submissions-- just check for the existence of
        # an ActivityState referring to this quiz.
        try:
            state = ActivityState.objects.get(user=user)
            if (len(state.json) > 0):
                return True
        except ActivityState.DoesNotExist:
            return False

    def edit_form(self):
        class EditForm(forms.Form):
            description = forms.CharField(widget=forms.widgets.Textarea(),
                                          initial=self.description)
            rhetorical = forms.BooleanField(initial=self.rhetorical)
            alt_text = "<a href=\"" + \
                reverse("edit-quiz", args=[self.id]) + \
                "\">manage questions/answers</a>"
        return EditForm()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            description = forms.CharField(widget=forms.widgets.Textarea())
            rhetorical = forms.BooleanField()
        return AddForm()

    @classmethod
    def create(self, request):
        return Quiz.objects.create(
            description=request.POST.get('description', ''),
            rhetorical=request.POST.get('rhetorical', ''))

    def edit(self, vals, files):
        self.description = vals.get('description', '')
        self.rhetorical = vals.get('rhetorical', '')
        self.save()

    def add_question_form(self, request=None):
        class AddQuestionForm(forms.ModelForm):

            class Meta:
                model = Question
                exclude = ("quiz", "ordinality")
        return AddQuestionForm(request)

    def update_questions_order(self, question_ids):
        for i, qid in enumerate(question_ids):
            question = Question.objects.get(id=qid)
            question.ordinality = i + 1
            question.save()

    def questions(self):
        return self.question_set.all().prefetch_related('answer_set')

    def required_questions(self):
        return self.question_set.filter(
            required=True).order_by('id').prefetch_related('answer_set')

    def optional_questions(self):
        return self.question_set.filter(
            optional=True).order_by('id').prefetch_related('answer_set')


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=256,
                                     choices=(
                                         ("multiple choice",
                                          "Multiple Choice: Multiple answers"),
                                         ("single choice",
                                          "Multiple Choice: Single answer"),
                                         ("short text", "Short Text"),
                                         ("long text", "Long Text"),
                                     ))
    ordinality = models.IntegerField(default=1)
    explanation = models.TextField(blank=True)
    intro_text = models.TextField(blank=True)

    required = models.BooleanField(default=False)
    optional = models.BooleanField(default=False)

    class Meta:
        ordering = ('quiz', 'ordinality')

    def __str__(self):
        return (
            smart_str(
                self.quiz.pageblock()
            ) + (
                ": %d " %
                self.ordinality) + " " + self.text[0:30] + "..."
        )

    def add_answer_form(self, request=None):
        class AddAnswerForm(forms.ModelForm):

            class Meta:
                model = Answer
                exclude = ("question", "ordinality")
        return AddAnswerForm(request)

    def correct_answer(self):
        if self.question_type != "single choice":
            return None

        return self.answer_set.filter(correct=True).first()

    def correct_answer_number(self):
        if self.question_type != "single choice":
            return None
        return self.answer_set.filter(correct=True)[0].ordinality

    def correct_answer_value(self):
        if self.question_type != "single choice":
            return None
        return self.answer_set.filter(correct=True)[0].value

    def correct_answer_letter(self):
        if (self.question_type != "single choice" or
                self.answer_set.count() == 0):
            return None

        return chr(ord('A') + self.correct_answer_number() - 1)

    def update_answers_order(self, answer_ids):
        for i, aid in enumerate(answer_ids):
            answer = Answer.objects.get(id=aid)
            answer.ordinality = i + 1
            answer.save()

    def short_text(self):
        return self.text[0:36]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ordinality = models.IntegerField(default=1)
    value = models.CharField(max_length=256, blank=True)
    label = models.TextField(blank=True)
    correct = models.BooleanField(default=False)

    class Meta:
        ordering = ('question', 'ordinality')

    def __str__(self):
        return self.label

    def letter(self):
        return chr(ord('A') + self.ordinality - 1)


class Submission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted = models.DateTimeField(default=timezone.now)


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    value = models.TextField(blank=True)

    def __str__(self):
        return (
            "response to %s by %s at %s" % (
                smart_str(self.question),
                smart_str(self.user),
                self.submitted)
        )


class ActivityState(models.Model):
    user = models.ForeignKey(
        User, related_name="quiz_user", on_delete=models.CASCADE)
    json = models.TextField(blank=True)
    submitted = models.DateTimeField(default=timezone.now)

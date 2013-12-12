from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock
from django import forms
from django.contrib.sites.models import Site


class Case(models.Model):
    name = models.CharField(max_length=25)


class Block(models.Model):
    pageblocks = generic.GenericRelation(
        PageBlock,
        related_name="taking_action_pageblocks")
    case_name = models.CharField(max_length=25)
    show_correct = models.BooleanField(default=False)
    template_file = "activity_taking_action/taking_action.html"
    display_name = "Activity: Taking Action"

    # list of steps
    list_of_steps = [
        'review_case_history',
        'analyze_action_criteria',
        'choose_action',
        'next_steps',
        'complete_report_overview',
        'complete_report_top_of_form',
        'complete_report_middle_of_form',
        'complete_report_bottom_of_form',
        'complete_report_nice_work',
        'complete_report_expert',
        'case_summary'
    ]

    list_of_steps_json = simplejson.dumps(list_of_steps)
    templates_by_step = [(a, "activity_taking_action/step_%s.html" % a)
                         for a in list_of_steps]

    def site(self):
        return Site.objects.get_current()

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            case_name = forms.CharField()
            show_correct = forms.BooleanField()
        return AddForm()

    @classmethod
    def create(self, request):
        name = request.POST.get('case_name', '')
        return Block.objects.create(case_name=name)

    def edit_form(self):
        class EditForm(forms.Form):
            case_name = forms.CharField(initial=self.case_name)
        return EditForm()

    def edit(self, vals, files):
        self.case_name = vals.get('case_name', '')
        self.save()

    def case(self):
        return Case.objects.filter(name=self.case_name).order_by('id')


class ActivityState (models.Model):
    user = models.ForeignKey(User, related_name="taking_action_user")
    json = models.TextField(blank=True)


def score_on_taking_action(the_student):
    """For now just report complete if the user has attempted to fill
    out LDSS form."""
    try:
        #import pdb
        # pdb.set_trace()
        if len(the_student.taking_action_user.all()) > 0:
            if 'complete' in simplejson.loads(
                    the_student.taking_action_user.all()[0].json):
                return 'completed_form'  # did they complete the form?
            else:
                return 'clicked_through'
        else:
            return 'no_data'
    except:
        return 'no_data'

from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock
from django import forms
from django.contrib.sites.models import Site


class Case(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(
        verbose_name="image",
        upload_to="media/img/" +
        "/%Y/%m/%d/",
        null=True,
        blank=True)
    case_history = models.TextField()
    correct_answer = models.CharField(max_length=25)
    explanation = models.TextField()
    factors_for_decision = models.TextField()

    def __unicode__(self):
        return (
            "%s: \"%s[...]%s\"" % (
                self.name,
                self.case_history[:16],
                self.case_history[-16:])
        )


class Block(models.Model):
    pageblocks = generic.GenericRelation(
        PageBlock,
        related_name="bruise_recon_pageblocks")
    case_name = models.CharField(max_length=25)
    show_correct = models.BooleanField(default=False)
    template_file = "activity_bruise_recon/bruise_recon.html"
    display_name = "Activity: Bruise Recognition"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def site(self):
        return Site.objects.get_current()

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
        return Case.objects.get(name=self.case_name)


class ActivityState (models.Model):
    user = models.ForeignKey(User, related_name="bruise_recon_user")
    json = models.TextField(blank=True)


def score_on_bruise_recon(the_student):
    try:
        if len(the_student.bruise_recon_user.all()) > 0:
            recon_json = simplejson.loads(
                the_student.bruise_recon_user.all()[0].json)
            bruise_recon_score_info = dict(
                [(a.strip(), b['score'])
                 for a, b
                 in recon_json.iteritems()
                 if a.strip() != '' and 'score' in b])
            return sum(bruise_recon_score_info.values())
        else:
            return None
    except:
        return None

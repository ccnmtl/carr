from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock, Section
from django import forms
from django.contrib.sites.models import Site, RequestSite

class Case(models.Model):
    name = models.CharField(max_length=25)


class Block(models.Model):
    pageblocks = generic.GenericRelation(PageBlock, related_name="taking_action_pageblocks")
    case_name = models.CharField(max_length=25)
    show_correct = models.BooleanField(default=False)
    template_file = "activity_taking_action/taking_action.html"
    display_name = "Activity: Taking Action"
    
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
    def create(self,request):
        name = request.POST.get('case_name','')
        return Block.objects.create(case_name=name)
    
    def edit_form(self):
        class EditForm(forms.Form):
            case_name = forms.CharField(initial=self.case_name)
        return EditForm();
    
    def edit(self,vals,files):
        case_name = vals.get('case_name','')
        self.save()
        
    def case(self):
        return case.objects.filter(name=self.case_name).order_by('id')

    
class ActivityState (models.Model):
    user = models.ForeignKey(User, related_name="taking_action_user")
    json = models.TextField(blank=True)


    

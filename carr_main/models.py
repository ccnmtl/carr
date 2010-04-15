from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from pagetree.models import PageBlock, Section
from pageblocks.models import PullQuoteBlock
from django import forms
from django.db.models.signals import post_save
from django.contrib.sites.models import Site


class SiteState(models.Model):
    user = models.ForeignKey(User, related_name="application_user")
    last_location = models.CharField(max_length=255)
    visited = models.TextField()
    
    def __init__(self, *args, **kwargs):
        super(SiteState, self).__init__(*args, **kwargs)
        
        if (len(self.visited) > 0): 
            self.state_object = simplejson.loads(self.visited)
        else:
            self.state_object = {}
    
    def get_has_visited(self, section):
        has_visited = self.state_object.has_key(str(section.id))
        return has_visited
    
    def set_has_visited(self, sections):
        for s in sections:
            self.state_object[str(s.id)] = s.label
            
        self.visited = simplejson.dumps(self.state_object)
        self.save()
    
    def save_last_location(self, path, section):
        self.state_object[str(section.id)] = section.label
        self.last_location = path
        self.visited = simplejson.dumps(self.state_object)
        self.save()    
        
        
        
class SiteSection(Section):
    
    sites = models.ManyToManyField(Site)
    
    def __unicode__(self):
        return self.label
        
    def site_section_nav (self, traversal_function):
        """ traverse the tree until you can return a page that visible on the current site"""

        

        
        x = self
        
        while traversal_function(x):
            x = traversal_function(x).section_site()
            if Site.objects.get(id=settings.SITE_ID) in x.sites.all():
                return x
        return None
        
    def get_next_site_section(self):
        return self.site_section_nav (lambda x: x.get_next())
    
    def get_previous_site_section(self):
        return self.site_section_nav (lambda x: x.get_previous_leaf())
        
Section.section_site =                  lambda x : SiteSection.objects.get(section_ptr=x)
Section.sites =                         lambda x : x.section_site().sites.all()
Section.get_previous_site_section =     lambda x : x.section_site().get_previous_site_section()
Section.get_next_site_section =         lambda x : x.section_site().get_next_site_section()
            
def find_or_add_site_section(**kwargs):
    new_section = kwargs['instance']
    if len(SiteSection.objects.filter(section_ptr=new_section)) == 0:
    
        new_site_section = SiteSection (section_ptr=new_section)
        new_site_section.__dict__.update(new_section.__dict__)
        
        #pages are visible on all sites by default:
        new_site_section.sites = Site.objects.all()            
        new_site_section.save()
        
post_save.connect(find_or_add_site_section, Section)


class FlashVideoBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    file_url = models.CharField(max_length=512)
    image_url = models.CharField(max_length=512)
    width = models.IntegerField()
    height = models.IntegerField()
    
    template_file = "carr_main/flashvideoblock.html"
    display_name = "Flash Video (using JW Player)"


    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def edit_form(self):
        class EditForm(forms.Form):
            file_url = forms.CharField(initial=self.file_url)
            image_url = forms.CharField(initial=self.image_url)
            width = forms.IntegerField(initial=self.width)
            height = forms.IntegerField(initial=self.height)
        return EditForm()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            file_url = forms.CharField()
            image_url = forms.CharField()
            width = forms.IntegerField()
            height = forms.IntegerField()
        return AddForm()

    @classmethod
    def create(self,request):
        return FlashVideoBlock.objects.create(file_url=request.POST.get('file_url',''), 
                                              image_url=request.POST.get('image_url',''),
                                              width=request.POST.get('width', ''),
                                              height=request.POST.get('height', ''))

    def edit(self,vals,files):
        self.file_url = vals.get('file_url','')
        self.image_url = vals.get('image_url','')
        self.width = vals.get('width','')
        self.height = vals.get('height','')
        self.save()
        
        
        


class PullQuoteBlock_2 (PullQuoteBlock):
    template_file = "admin/pageblocks/pullquoteblock_2.html"
    #template_file = "pageblocks/pullquoteblock_2.html"
    display_name = "Pull Quote Type 2"
    @classmethod
    def create(self,request):
        return PullQuoteBlock_2.objects.create(body=request.POST.get('body',''))


class PullQuoteBlock_3 (PullQuoteBlock):
    template_file = "admin/pageblocks/pullquoteblock_3.html"
    
    #template_file = "pageblocks/pullquoteblock_3.html"
    display_name = "Pull Quote Type 3"

    @classmethod
    def create(self,request):
        return PullQuoteBlock_3.objects.create(body=request.POST.get('body',''))

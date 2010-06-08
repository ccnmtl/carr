from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from pagetree.models import PageBlock, Section, SectionChildren
from pageblocks.models import PullQuoteBlock
from django import forms
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.contrib.auth.models import User, Group

import re, pdb


def user_type(self):
    if cache.get("user_type_%d" % self.id):
        #print "user type found in cache."
        return cache.get("user_type_%d" % self.id)
    result = None
    if len( [ g for g in self.groups.all() if 'tlcxml' in  g.name]) > 0:
        #TODO: also give admin to all people marked such in the admin user interface.
        result = 'admin'
    elif len( [ g for g in self.groups.all() if '.fc.' in  g.name]) > 0:
        result = 'faculty'
    else:
        result = 'student'
    cache.set("user_type_%d" % self.id,result,60*60*24)
    #print "user type stored in cache."
    return result

        
def classes_i_teach(self):
    if cache.get("classes_i_teach_%d" % self.id):
        #print "classes_i_teach found in cache."
        return cache.get("classes_i_teach_%d" % self.id)
        
    my_classes = [re.match('t(\d).y(\d{4}).s(\d{3}).c(\w)(\d{4}).(\w{4}).(\w{2})',c.name)    for c in self.groups.all()]
    result = [(a.groups()[0:6] ) for a in my_classes if a != None and a.groups()[6] == 'fc']
    cache.set("classes_i_teach_%d" % self.id,result,30)
    return result
    
def classes_i_take(self):
    if cache.get("classes_i_take_%d" % self.id):
        #print "classes_i_take found in cache."
        return cache.get("classes_i_take_%d" % self.id)
    my_classes = [re.match('t(\d).y(\d{4}).s(\d{3}).c(\w)(\d{4}).(\w{4}).(\w{2})',c.name)    for c in self.groups.all()]
    result = [(a.groups()[0:6] ) for a in my_classes if a != None and a.groups()[6] == 'st']
    cache.set("classes_i_take_%d" % self.id,result,30)
    return result

def students_i_teach (self):
    if cache.get("students_i_teach_%d" % self.id):
        #print "students_i_teach found in cache."
        return cache.get("students_i_teach_%d" % self.id)
    the_classes_i_teach = self.classes_i_teach()
    # yeah, the people who take more than zero of the classes I teach.
    result = [ u for u in User.objects.all()  if len([c for c in u.classes_i_take() if c in the_classes_i_teach]) > 0  and u != self]
    cache.set("students_i_teach_%d" % self.id,result,30)
    return result


def is_taking (self, course_info):
    course_string = "t%s.y%s.s%s.c%s%s.%s" % course_info
    list_of_wind_affils = [g.name for g in self.groups.all()]
    for w in list_of_wind_affils:
        if course_string in w:
            return True
    return False;
    
def students_in_class(course_info):
    cache_key = "students_in_t%s.y%s.s%s.c%s%s.%s" % course_info
    
    if cache.get(cache_key):
        #print "students_in_class found in cache."
        return cache.get(cache_key)
    result = []
    all_affils = Group.objects.all()
    f_lookup = "t%s.y%s.s%s.c%s%s.%s.fc"
    s_lookup = "t%s.y%s.s%s.c%s%s.%s.st"
    faculty_affils_list = [a for a in all_affils if f_lookup % course_info in a.name]
    student_affils_list = [a for a in all_affils if s_lookup % course_info in a.name]
    if faculty_affils_list and student_affils_list:
        faculty =  faculty_affils_list[0].user_set.all()
        students = student_affils_list[0].user_set.all()
        result = [s for s in students if s not in faculty]
    
    cache.set(cache_key,result,30)
    return result
   

def number_of_students_in_class (course_info):
    return len(students_in_class(course_info))

        
User.user_type = user_type
User.classes_i_teach = classes_i_teach        
User.classes_i_take = classes_i_take
User.students_i_teach = students_i_teach
User.is_taking = is_taking






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
            #if Site.objects.get(id=settings.SITE_ID) in x.sites.all():
            #    return x
            #if x.in_site():
            #    return x
            if settings.SITE_ID in [s.id for s in x.sites.all()]:
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
Section.in_site =                       lambda x: settings.SITE_ID in [s.id for s in x.sites()]

def new_get_children(self):
    return [sc.child for sc in SectionChildren.objects.filter(parent=self).order_by("ordinality") if sc.child.in_site()]

Section.get_children = new_get_children



            
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

from django.conf import settings
from django.db import models
import json
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from pagetree.models import PageBlock, Section, SectionChildren
from pageblocks.models import PullQuoteBlock
from django import forms
from django.db.models.signals import post_save
from django.core.cache import cache
from django.contrib.auth.models import User, Group

import re

course_re = '.*t(\d).y(\d{4}).s(\w{3}).c(\w)(\d{4}).(\w{4}).(\w{2}).*'


def user_sort_key(student):
    if student.last_name:
        return student.last_name
    else:
        return student.username


def sort_users(users):
    return sorted(users, key=user_sort_key)


def user_type(u):
    result = None
    if u is None:
        return None

    # Can run tests.
    elif len([g for g in u.groups.all() if 'tlcxml' in g.name]) > 0:
        result = 'admin'

    # Can view all student scores:
    elif len([g for g in u.groups.all() if '.fc.' in g.name]) > 0:
        result = 'faculty'
    # so we can easily grant this priviledge to people who are not actually
    # teaching a class:
    elif u.is_staff:
        result = 'faculty'
    elif u.username in settings.DEFAULT_SOCIALWORK_FACULTY_UNIS:
        result = 'faculty'

    # Can take the training, view own scores.
    else:
        result = 'student'

    return result


def classes_i_teach(u):
    cache_key = "classes_i_teach_%d" % u.id
    cached = cache.get(cache_key)
    if cached:
        return cached

    my_classes = [re.match(course_re, c.name) for c in u.groups.all()]
    result = [(a.groups()[0:6])
              for a in my_classes if a is not None and a.groups()[6] == 'fc']
    cache.set(cache_key, result, 30)
    return result


def classes_i_take(u):
    cache_key = "classes_i_take_%d" % u.id
    cached = cache.get(cache_key)
    if cached:
        return cached
    my_classes = [re.match(course_re, c.name) for c in u.groups.all()]
    result = [(a.groups()[0:6])
              for a in my_classes if a is not None and a.groups()[6] == 'st']
    cache.set(cache_key, result, 30)
    return result


def students_in_class(course_info):
    cache_key = "students_in_t%s.y%s.s%s.c%s%s.%s" % course_info
    cached = cache.get(cache_key)
    if cached:
        return cached
    result = []
    all_affils = Group.objects.all()
    f_lookup = "t%s.y%s.s%s.c%s%s.%s.fc"
    s_lookup = "t%s.y%s.s%s.c%s%s.%s.st"
    faculty_affils_list = [
        a for a in all_affils if f_lookup %
        course_info in a.name]
    student_affils_list = [
        a for a in all_affils if s_lookup %
        course_info in a.name]
    if faculty_affils_list and student_affils_list:
        faculty = faculty_affils_list[0].user_set.all()
        students = student_affils_list[0].user_set.all()
        result = sort_users([s for s in students if s not in faculty])

    cache.set(cache_key, result, 30)
    return result


def number_of_students_in_class(course_info):
    return len(students_in_class(course_info))


def users_by_uni(uni_string):
    return sort_users(User.objects.filter(username__icontains=uni_string))


class SiteState(models.Model):
    user = models.ForeignKey(User, related_name="application_user")
    last_location = models.CharField(max_length=255)

    visited = models.TextField()

    def __init__(self, *args, **kwargs):
        super(SiteState, self).__init__(*args, **kwargs)

        if (len(self.visited) > 0):
            self.state_object = json.loads(self.visited)
        else:
            self.state_object = {}

    def get_has_visited(self, section):
        has_visited = str(section.id) in self.state_object
        return has_visited

    def set_has_visited(self, sections):
        for s in sections:
            self.state_object[str(s.id)] = s.label

        self.visited = json.dumps(self.state_object)
        self.save()

    def save_last_location(self, path, section):
        if len([a for a in Site.objects.all()
                if a not in section.section_site().sites.all()]) > 0:
            return
        self.state_object[str(section.id)] = section.label
        self.last_location = path
        self.visited = json.dumps(self.state_object)
        self.save()


class SiteSection(Section):

    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return self.label

    def site_section_nav(self, traversal_function):
        """ traverse the tree until you can return a page that visible
        on the current site"""
        x = self
        while traversal_function(x):
            x = traversal_function(x).section_site()
            if settings.SITE_ID in [s.id for s in x.sites.all()]:
                return x
        return None

    def get_next_site_section(self):
        return self.site_section_nav(lambda x: x.get_next())

    def get_previous_site_section(self):
        return self.site_section_nav(lambda x: x.get_previous_leaf())


def section_site(x):
    return SiteSection.objects.get(section_ptr=x)


def get_previous_site_section(x):
    return section_site(x).get_previous_site_section()


def get_next_site_section(x):
    return section_site(x).get_next_site_section()


Section.sites = lambda x: section_site(x).sites.all()


def in_site(x):
    return settings.SITE_ID in [s.id for s in x.sites()]


def new_get_children(self):
    return (
        [sc.child for sc in SectionChildren.objects.filter(
            parent=self).order_by("ordinality") if in_site(sc)]
    )
Section.get_children = new_get_children


def new_get_siblings(self):
    return (
        [sc.child for sc in SectionChildren.objects.filter(
            parent=self.get_parent()) if in_site(sc.child)]
    )
Section.get_siblings = new_get_siblings


def find_or_add_site_section(**kwargs):
    new_section = kwargs['instance']
    if len(SiteSection.objects.filter(section_ptr=new_section)) == 0:

        new_site_section = SiteSection(section_ptr=new_section)
        new_site_section.__dict__.update(new_section.__dict__)

        # pages are visible on all sites by default:
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
    def create(self, request):
        return FlashVideoBlock.objects.create(
            file_url=request.POST.get('file_url', ''),
            image_url=request.POST.get(
                'image_url',
                ''),
            width=request.POST.get(
                'width',
                ''),
            height=request.POST.get('height', ''))

    def edit(self, vals, files):
        self.file_url = vals.get('file_url', '')
        self.image_url = vals.get('image_url', '')
        self.width = vals.get('width', '')
        self.height = vals.get('height', '')
        self.save()


class PullQuoteBlock_2 (PullQuoteBlock):
    template_file = "admin/pageblocks/pullquoteblock_2.html"
    display_name = "Pull Quote Type 2"

    @classmethod
    def create(self, request):
        return (
            PullQuoteBlock_2.objects.create(body=request.POST.get('body', ''))
        )


class PullQuoteBlock_3 (PullQuoteBlock):
    template_file = "admin/pageblocks/pullquoteblock_3.html"

    display_name = "Pull Quote Type 3"

    @classmethod
    def create(self, request):
        return (
            PullQuoteBlock_3.objects.create(body=request.POST.get('body', ''))
        )

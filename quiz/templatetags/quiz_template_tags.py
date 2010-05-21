from django import template
from djangohelpers.templatetags import TemplateTagNode
from quiz.models import *
from carr_main.models import *
import pdb


register = template.Library()



class GetCourses(TemplateTagNode):
    noun_for = {"for": "quiz_label", 'in': 'obj'}

    def __init__(self, varname, quiz_label, obj):
        TemplateTagNode.__init__(self, varname, quiz_label=quiz_label, obj=obj)

    def execute_query(self, quiz_label, obj):
        try:
            return [ o for o in obj if  o['quiz'].label().lower() == quiz_label.lower()][0]
        except:
            return None
        
register.tag('get_courses', GetCourses.process_tag)



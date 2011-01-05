from django import template
from djangohelpers.templatetags import TemplateTagNode
from quiz.models import *
from quiz.templatetags import GetScores
from carr_main.models import *

register = template.Library()
        
register.tag('get_scores', GetScores.process_tag)



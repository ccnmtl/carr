from django import template
from quiz.templatetags import GetScores

register = template.Library()

register.tag('get_scores', GetScores.process_tag)

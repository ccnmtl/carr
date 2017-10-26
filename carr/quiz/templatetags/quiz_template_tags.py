from django import template
from djangohelpers.templatetags import TemplateTagNode

register = template.Library()


class GetScores(TemplateTagNode):
    noun_for = {"for": "quiz_label", 'in': 'obj'}

    def __init__(self, varname, quiz_label, obj):
        TemplateTagNode.__init__(self, varname, quiz_label=quiz_label, obj=obj)

    def execute_query(self, quiz_label, obj):
        try:
            return (
                [o for o in obj if o['quiz']
                    .label().lower() == quiz_label.lower()][0]
            )
        except (KeyError, IndexError):
            return None


register.tag('get_scores', GetScores.process_tag)

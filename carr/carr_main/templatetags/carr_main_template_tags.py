from django import template
from django.conf import settings
from django.template.loader import get_template
from pagetree.templatetags.render import RenderNode

from carr.carr_main.models import classes_i_take as classes_i_take_f
from carr.carr_main.models import classes_i_teach as classes_i_teach_f
from carr.carr_main.models import user_type as user_type_f


register = template.Library()


@register.simple_tag
def media_url():
    return settings.MEDIA_URL


@register.assignment_tag
def user_type(user, *args):
    return user_type_f(user)


@register.assignment_tag
def classes_i_teach(user, *args):
    return classes_i_teach_f(user)


@register.assignment_tag
def classes_i_take(user, *args):
    return classes_i_take_f(user)


class RenderJSNode(RenderNode):

    def render(self, context):
        content_object = context[self.block].content_object
        if hasattr(content_object, 'js_template_file'):
            t = get_template(getattr(content_object, 'js_template_file'))
            d = {}
            d['block'] = content_object
            return t.render(d)
        else:
            return ""


@register.tag('renderjs')
def renderjs(parser, token):
    block = token.split_contents()[1:][0]
    return RenderJSNode(block)

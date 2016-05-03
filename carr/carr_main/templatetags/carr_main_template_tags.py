from django import template
from django.conf import settings
from carr.carr_main.models import user_type as user_type_f
from carr.carr_main.models import classes_i_teach as classes_i_teach_f
from carr.carr_main.models import classes_i_take as classes_i_take_f

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

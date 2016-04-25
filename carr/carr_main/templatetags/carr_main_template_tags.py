from django import template
from django.conf import settings
from carr.carr_main.models import user_type as user_type_f

register = template.Library()


@register.simple_tag
def media_url():
    return settings.MEDIA_URL


@register.simple_tag
def user_type(user, *args):
    return user_type_f(user)

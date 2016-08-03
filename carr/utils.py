from django.conf import settings
from django.contrib.auth.models import User


def state_json(state_class, user):
    doc = '{}'
    try:
        state = state_class.objects.get(user=user)
        if (len(state.json) > 0):
            doc = state.json
    except state_class.DoesNotExist:
        pass

    return doc


def get_students():
    return User.objects.filter(is_staff=False).exclude(
        groups__name__contains='tlcxml'
    ).exclude(
        groups__name__contains='.fc.'
    ).exclude(
        username__in=settings.DEFAULT_SOCIALWORK_FACULTY_UNIS
    ).order_by('last_name', 'username')


def filter_users_by_affiliation(affiliation, the_users):
    regex = r'^\w+\.\w+\.\w+\.\w+\.intc.*'
    if affiliation == 'dental':
        return the_users.filter(groups__name__regex=regex)
    else:
        return the_users.exclude(groups__name__regex=regex)

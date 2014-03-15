from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.http import urlquote
from django.conf import settings

from courseaffils.models import Course
from django.db.models import get_model

Collaboration = get_model('structuredcollaboration', 'collaboration')

SESSION_KEY = 'ccnmtl.courseaffils.course'


def is_anonymous_path(current_path):
    if hasattr(settings, 'COURSEAFFILS_PATHS'):
        for path in settings.COURSEAFFILS_PATHS:
            if isinstance(path, str):
                if current_path.startswith(path):
                    return False
            elif hasattr(path, 'match'):
                #regex
                if path.match(current_path):
                    return False

    if not hasattr(settings, 'COURSEAFFILS_EXEMPT_PATHS'):
        return False

    for exempt_path in settings.COURSEAFFILS_EXEMPT_PATHS:
        try:
            if current_path.startswith(exempt_path):
                return True
        except TypeError:  # it wasn't a string object .. must be a regex
            if exempt_path.match(current_path):
                return True

    #if whitelist, then default is to anonymous path
    return hasattr(settings, 'COURSEAFFILS_PATHS')


class CourseManagerMiddleware(object):
    def process_request(self, request):
        request.course = None  # must be present to be a caching key

        if is_anonymous_path(request.path):
            return None

        if not request.user.is_authenticated():
            return None

        if 'unset_course' in request.GET:
            if SESSION_KEY in request.session:
                del request.session[SESSION_KEY]

        def decorate_request(request, course):
            request.course = course
            request.coursename = course.title

        if 'set_course' in request.GET:
            request.session[SESSION_KEY] = course = \
                Course.objects.get(group__name=request.GET['set_course'])
            decorate_request(request, course)

            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])

            return None

        if SESSION_KEY in request.session:
            course = request.session[SESSION_KEY]
            decorate_request(request, course)
            return None

        available_courses = Course.objects.filter(group__user=request.user)

        if len(available_courses) == 1:
            request.session[SESSION_KEY] = course = \
                available_courses[0]
            decorate_request(request, course)
            return None

        if len(available_courses) == 0:
            return render_to_response('courseaffils/no_courses.html',
                                      {'request': request,
                                       'user': request.user,
                                       })

        next_redirect = ''
        if ('QUERY_STRING' in request.META and
                not 'unset_course' in request.GET):
            next_redirect = '&next=%s' % urlquote(request.get_full_path())

        context = {
            'courses': available_courses,
            'user': request.user,
            'request': request,
            'next': next_redirect,
        }

        return render_to_response('courseaffils/select_course.html', context)

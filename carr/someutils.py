#!ve/bin/python

try:
    from django.conf import settings
    from django.contrib.auth import REDIRECT_FIELD_NAME
    from django.utils.http import urlquote
    from django.http import HttpResponseRedirect

    def match_path(path, config_string):
        config_list = getattr(settings, config_string, [])
        for p in config_list:
            if isinstance(p, str) and path.startswith(p):
                return True
            elif hasattr(p, 'match') and p.match(path):
                return True
        return False

    class AuthRequirementMiddleware(object):

        def process_request(self, request):
            path = urlquote(request.get_full_path())
            if request.user.is_authenticated():
                return None

            if match_path(path, 'ANONYMOUS_PATHS'):
                return None
            if hasattr(settings, 'NON_ANONYMOUS_PATHS') \
                    and not match_path(path, 'NON_ANONYMOUS_PATHS'):
                return None

            return HttpResponseRedirect('%s?%s=%s' % (
                settings.LOGIN_URL,
                REDIRECT_FIELD_NAME,
                path))

except ImportError:
    pass

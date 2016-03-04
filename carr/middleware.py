from django.conf import settings
from django.contrib.sites.requests import RequestSite


class SiteIdMiddleware(object):
    def process_request(self, request):
        if 'ssw' in RequestSite(request).domain:
            settings.SITE_ID = 2
        else:
            settings.SITE_ID = 2

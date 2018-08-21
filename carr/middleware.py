from django.conf import settings
from django.contrib.sites.requests import RequestSite


class SiteIdMiddleware(object):
    def process_request(self, request):
        if 'ssw' in RequestSite(request).domain:
            settings.SITE_ID = settings.SITE_SOCIAL_WORK  # 2
        elif 'cdm' in RequestSite(request).domain:
            settings.SITE_ID = settings.SITE_DENTAL  # 1

        # otherwise default to whatever is already set

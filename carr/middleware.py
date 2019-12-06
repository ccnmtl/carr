from django.conf import settings
from django.contrib.sites.requests import RequestSite
from django.utils.deprecation import MiddlewareMixin


class SiteIdMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if 'ssw' in RequestSite(request).domain:
            settings.SITE_ID = settings.SITE_SOCIAL_WORK  # 2
        elif 'cdm' in RequestSite(request).domain:
            settings.SITE_ID = settings.SITE_DENTAL  # 1

from django.contrib import sitemaps
from django.urls import reverse

from wagtail.contrib.sitemaps import Sitemap as WagtailSitemap
from wagtail.core.models import Page

import datetime


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['search']

    def location(self, obj):
        return reverse(obj)

    def lastmod(self, obj):
        return datetime.datetime.now()


class SchoolsSitemap(WagtailSitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        page = Page.objects.get(pk=16)

        site = self.get_wagtail_site()
        site.root_page = page

        pages = site.root_page.get_descendants(inclusive=True).live().public().order_by('path').specific()

        return (pages)

    def location(self, obj):
        return reverse(obj)

    def lastmod(self, obj):
        return datetime.datetime.now()


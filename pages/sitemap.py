from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from article.models import Post
from mike_admin.models import Service


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated_on
    
class ServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Service.objects.all()

    def lastmod(self, obj):
        return obj.date_modified

class ImportantSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['pages:index']

    def location(self, item):
        return reverse(item)
    
class AuthViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['mike_admin:login', 'mike_admin:django_registration_register']

    def location(self, item):
        return reverse(item)

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['pages:contact', 'pages:shop', 'pages:articles', 'pages:terms']

    def location(self, item):
        return reverse(item)
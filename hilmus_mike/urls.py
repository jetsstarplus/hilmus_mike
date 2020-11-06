
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from django.conf import settings
from django.conf.urls.static import static

import mike_admin.urls
import pages.urls
import daraja.urls

from article.sitemap import PostSitemap

sitemaps = {
    'PostSitemap':PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('account/', include(mike_admin.urls)),
    path('article/', include('article.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('', include(pages.urls)),
    path('filer/', include('filer.urls')),
    path('', include('daraja.urls')),
    path('', include('daraja.api.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from fbf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    url(r'', include('meta.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]

# Get Django to serve media files in debug mode.
if settings.DEBUG:
    urlpatterns += [url(r'^resources/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]

if not settings.DEBUG:
    urlpatterns += [
        url(r'^resources/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    ]

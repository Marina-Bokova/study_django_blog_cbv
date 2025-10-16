from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from apps.blog.feeds import LatestPostFeed

handler403 = 'apps.blog.views.tr_handler403'
handler404 = 'apps.blog.views.tr_handler404'
handler500 = 'apps.blog.views.tr_handler500'

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('feeds/latest/', LatestPostFeed(), name='latest_post_feed'),
    path('', include('apps.blog.urls')),
    path('', include('apps.accounts.urls')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

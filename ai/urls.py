from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^result/(?P<pk>[0-9]+)/$', views.index, name = "index"),
    url(r'^api/msg=(?P<msg>.+?)&id=(?P<idu>.*?)/$', views.ajax_view, name = "res"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)

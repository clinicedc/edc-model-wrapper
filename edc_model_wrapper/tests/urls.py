from django.conf.urls import url
from django.views.generic.base import View

urlpatterns = [
    url(r'^listboard/(?P<f2>.)/(?P<f3>.)/',
        View.as_view(), name='listboard_url'),
    url(r'^listboard/(?P<example_identifier>.)/(?P<example_log>.)/',
        View.as_view(), name='listboard_url'),
    url(r'^listboard/', View.as_view(), name='listboard_url')
]

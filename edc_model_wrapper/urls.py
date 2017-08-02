from django.conf import settings
from django.conf.urls import url
from django.views.generic.base import View


if settings.APP_NAME == 'edc_model_wrapper':

    from .tests import edc_model_wrapper_admin

    urlpatterns = [
        url(r'^admin/', edc_model_wrapper_admin.urls),
        url(r'^listboard/(?P<f2>.)/(?P<f3>.)/',
            View.as_view(), name='listboard_url'),
        url(r'^listboard/', View.as_view(), name='listboard_url')
    ]

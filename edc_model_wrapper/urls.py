from django.conf import settings
from django.conf.urls import url, include


if settings.APP_NAME == 'edc_model_wrapper':

    from .tests import edc_model_wrapper_admin

    urlpatterns = [
        url(r'^admin/', edc_model_wrapper_admin.urls),
        url(r'^listboard/', include('edc_model_wrapper.tests.urls',
                                    namespace='edc-model-wrapper')),
    ]

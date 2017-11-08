from django.conf import settings
from django.urls.conf import path, include


if settings.APP_NAME == 'edc_model_wrapper':

    from .tests import edc_model_wrapper_admin

    urlpatterns = [
        path('admin/', edc_model_wrapper_admin.urls),
        path('listboard/', include('edc_model_wrapper.tests.urls'),
             name='listboard_url'),
    ]

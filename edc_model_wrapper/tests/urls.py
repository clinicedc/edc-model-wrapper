from django.urls.conf import path, include
from django.views.generic.base import View
from django.urls.conf import re_path

from .admin import edc_model_wrapper_admin

app_name = "edc_model_wrapper"

urlpatterns = [
    path("admin/", edc_model_wrapper_admin.urls),
    re_path(r"^listboard/(?P<f2>.)/(?P<f3>.)/", View.as_view(), name="listboard_url"),
    re_path(
        r"^listboard/(?P<example_identifier>.)/(?P<example_log>.)/",
        View.as_view(),
        name="listboard_url",
    ),
    re_path(r"^listboard/", View.as_view(), name="listboard_url"),
]


# urlpatterns = [
#     path("admin/", edc_model_wrapper_admin.urls),
#     path(
#         "listboard/", include("edc_model_wrapper.tests.urls"), name="listboard_url"
#     ),
# ]

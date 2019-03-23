from django.urls.conf import path
from django.views.generic.base import View
from django.urls.conf import re_path
from edc_dashboard import url_names

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

url_names.register("listboard_url", "listboard_url", "edc_model_wrapper")

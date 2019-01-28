from django.views.generic.base import View
from django.urls.conf import re_path

app_name = "edc_model_wrapper"

urlpatterns = [
    re_path(r"^listboard/(?P<f2>.)/(?P<f3>.)/", View.as_view(), name="listboard_url"),
    re_path(
        r"^listboard/(?P<example_identifier>.)/(?P<example_log>.)/",
        View.as_view(),
        name="listboard_url",
    ),
    re_path(r"^listboard/", View.as_view(), name="listboard_url"),
]

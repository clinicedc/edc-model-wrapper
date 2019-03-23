from copy import copy
from django.apps import apps as django_apps


class ModelWrapperTestHelper:

    dashboard_url = "/dashboard/"

    def __init__(
        self,
        model_wrapper=None,
        app_label=None,
        model=None,
        dashboard_url=None,
        model_obj=None,
        **kwargs,
    ):
        self.model_wrapper = model_wrapper
        self.dashboard_url = dashboard_url or self.dashboard_url
        if app_label:
            model = self.model_wrapper.model or model
            self.model_wrapper.model = f'{app_label}.{model.split(".")[1]}'
        self.model_wrapper.next_url_name = model_wrapper.next_url_name.split(":")[1]
        self.options = kwargs
        if model_obj:
            self.model_cls = model_obj.__class__
            self.model_obj = model_obj
        else:
            self.model_cls = django_apps.get_model(model_wrapper.model)
            self.model_obj = self.model_cls.objects.create(**self.options)

    def test(self, testcase):
        # add admin url
        wrapper = self.model_wrapper(model_obj=self.model_cls())
        testcase.assertIsNotNone(wrapper.href, msg="href")

        # add admin url
        wrapper = self.model_wrapper(model_obj=self.model_cls())
        testcase.assertIn("add", wrapper.href)

        # change admin url
        wrapper = self.model_wrapper(model_obj=copy(self.model_obj))
        testcase.assertIn("change", wrapper.href)

        # reverse
        testcase.assertIn(self.dashboard_url, wrapper.reverse())

        # next_url
        wrapper = self.model_wrapper(model_obj=copy(self.model_obj))
        testcase.assertIsNotNone(wrapper.href, msg="href")

        # querystring
        wrapper = self.model_wrapper(model_obj=copy(self.model_obj))
        for item in wrapper.querystring_attrs:
            testcase.assertIn(item, wrapper.querystring)
            testcase.assertIsNotNone(getattr(wrapper, item), msg=item)

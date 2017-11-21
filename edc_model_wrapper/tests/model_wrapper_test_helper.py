from django.apps import apps as django_apps


class ModelWrapperTestHelper:

    dashboard_url = '/dashboard/'

    def __init__(self, model_wrapper=None, **kwargs):
        self.model_wrapper = model_wrapper
        self.model_wrapper.model = model_wrapper.model_cls._meta.label_lower
        self.model_wrapper.next_url_name = (
            model_wrapper.next_url_name.split(':')[1])
        self.options = kwargs
        self.model = django_apps.get_model(model_wrapper.model)
        self.model_obj = self.model.objects.create(**self.options)

    def test(self, testcase):
        # add admin url
        wrapper = self.model_wrapper(model_obj=self.model())
        testcase.assertIsNotNone(wrapper.href, msg='href')

        # add admin url
        wrapper = self.model_wrapper(model_obj=self.model())
        testcase.assertIn('add', wrapper.href)

        # change admin url
        wrapper = self.model_wrapper(model_obj=self.model_obj)
        testcase.assertIn('change', wrapper.href)

        # reverse
        testcase.assertIn(self.dashboard_url, wrapper.reverse())

        # next_url
        wrapper = self.model_wrapper(model_obj=self.model_obj)
        testcase.assertIsNotNone(wrapper.next_url, msg='next_url')

        # querystring
        wrapper = self.model_wrapper(model_obj=self.model_obj)
        for item in wrapper.querystring_attrs:
            testcase.assertIn(item, wrapper.querystring)
            testcase.assertIsNotNone(getattr(wrapper, item), msg=item)

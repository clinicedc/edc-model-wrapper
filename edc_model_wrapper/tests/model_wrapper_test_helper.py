from django.apps import apps as django_apps


class ModelWrapperTestHelper:

<<<<<<< HEAD
    dashboard_url = '/dashboard/'

=======
>>>>>>> 88f2c98a68e280e3955d94335eb1f02e72083c4f
    def __init__(self, model_wrapper=None, app_label=None, **kwargs):
        self.model_wrapper = model_wrapper
        self.model_wrapper.model = f'{app_label}.{model_wrapper.model.split(".")[1]}'
        self.model_wrapper.next_url_name = (
            model_wrapper.next_url_name.split(':')[1])
        self.options = kwargs
        self.model = django_apps.get_model(model_wrapper.model)
        self.model_obj = self.model.objects.create(**self.options)

    def test(self, testcase):
        # add admin url
        wrapper = self.model_wrapper(model_obj=self.model())
        testcase.assertIsNotNone(wrapper.href)

        # add admin url
        wrapper = self.model_wrapper(model_obj=self.model())
        testcase.assertIn('add', wrapper.href)

        # change admin url
        wrapper = self.model_wrapper(model_obj=self.model_obj)
        testcase.assertIn('change', wrapper.href)

        # reverse
<<<<<<< HEAD
        testcase.assertIn(self.dashboard_url, wrapper.reverse())
=======
        testcase.assertIn('/dashboard/', wrapper.reverse())
>>>>>>> 88f2c98a68e280e3955d94335eb1f02e72083c4f

        # next_url
        wrapper = self.model_wrapper(model_obj=self.model_obj)
        testcase.assertIsNotNone(wrapper.next_url)

        # querystring
        wrapper = self.model_wrapper(model_obj=self.model_obj)
        for item in wrapper.querystring_attrs:
            testcase.assertIn(item, wrapper.querystring)
            testcase.assertIsNotNone(getattr(wrapper, item))

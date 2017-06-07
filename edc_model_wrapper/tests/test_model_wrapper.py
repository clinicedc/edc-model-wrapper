from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag

from ..wrappers import Fields, FieldWrapperError, FieldWrapperModelError
from ..wrappers import ModelWrapper, ModelWrapperObjectAlreadyWrapped, ModelWrapperModelError
from .models import Example, ParentExample, Appointment, SubjectVisit


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectVisit)
class SubjectVisitAdmin(admin.ModelAdmin):
    pass


@tag('fields')
class TestFields(TestCase):

    def test_fields_only_except_model(self):
        self.assertRaises(
            FieldWrapperError, Fields, model_obj=1, model=Example)

    def test_fields_only_except_models_with_name(self):
        self.assertRaises(
            FieldWrapperModelError, Fields, model_obj=Example(), model='blah')

    def test_fields(self):
        self.assertTrue(
            Fields(model_obj=Example(), model=Example))

    def test_fields_skips_example(self):
        class Wrapper:
            pass
        wrapper = Wrapper()
        fields = Fields(model_obj=ParentExample(), model=ParentExample)
        self.assertNotIn('example', dict(fields.fields(wrapper)))


@tag('model_wrapper')
class TestModelWrapper(TestCase):

    def test_model_wrapper(self):
        """Asserts can construct.
        """
        obj = Example()
        ModelWrapper(
            model_obj=obj, model=Example,
            next_url_name='thenexturl')

    def test_model_wrapper_bool(self):
        """Asserts obj can be truth tested.

        If model is not persisted is False.
        """
        obj = Example()
        ModelWrapper(
            model_obj=obj, model=Example,
            next_url_name='thenexturl')
        self.assertFalse(obj is True)

    def test_model_wrapper_wraps_once(self):
        """Asserts a wrapped model instance cannot be wrapped.
        """
        obj = Example()
        wrapper = ModelWrapper(
            model_obj=obj, model=Example,
            next_url_name='thenexturl')
        obj = wrapper.object
        self.assertRaises(
            ModelWrapperObjectAlreadyWrapped,
            ModelWrapper, model_obj=obj, model=Example,
            next_url_name='thenexturl')

    def test_model_wrapper_invalid_name_raises(self):
        """Asserts raises if model does not match model instance.
        """
        ModelWrapper(model_obj=Example(),
                     model='edc_model_wrapper.example',
                     next_url_name='thenexturl')
        self.assertRaises(
            ModelWrapperModelError,
            ModelWrapper, model_obj=Example(), model='blah', next_url_name='thenexturl')

    def test_model_wrapper_model_is_class1(self):
        """Asserts model returns as a class if passed label_lower.
        """
        wrapper = ModelWrapper(model_obj=Example(),
                               model='edc_model_wrapper.example',
                               next_url_name='thenexturl')
        self.assertEqual(wrapper.model, Example)

    def test_model_wrapper_model_is_class2(self):
        """Asserts model returns as a class if passed class.
        """
        wrapper = ModelWrapper(model_obj=Example(),
                               model=Example,
                               next_url_name='thenexturl')
        self.assertEqual(wrapper.model, Example)


class TestExampleWrappers(TestCase):

    def setUp(self):

        class ExampleModelWrapper(ModelWrapper):
            model = 'edc_model_wrapper.example'
            url_namespace = 'edc-model-wrapper'
            next_url_name = 'listboard_url'
            next_url_attrs = ['f1']
            querystring_attrs = ['f2', 'f3']
        self.wrapper_cls = ExampleModelWrapper

    def test_model_wrapper_model_object(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(wrapper.object, model_obj)

    def test_example_href(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.href,
            '/admin/edc_model_wrapper/example/add/?next=edc-model-wrapper:listboard_url,f1&f1=1&f2=2&f3=3')

    def test_model_wrapper_admin_urls_add(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.admin_url_name, 'edc-model-wrapper:admin:edc_model_wrapper_example_add')

    def test_model_wrapper_admin_urls_change(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.admin_url_name, 'edc-model-wrapper:admin:edc_model_wrapper_example_change')


@tag('1')
class TestExampleWrappers2(TestCase):
    """A group of tests that show a common scenario of 
    Appointment and SubjectVisit.
    """

    def setUp(self):

        class SubjectVisitModelWrapper1(ModelWrapper):
            model = 'edc_model_wrapper.subjectvisit'
            url_namespace = 'edc-model-wrapper'
            next_url_name = 'listboard_url'
            next_url_attrs = ['v1']
            # querystring_attrs = ['f2', 'f3']

        class SubjectVisitModelWrapper2(ModelWrapper):
            model = 'edc_model_wrapper.subjectvisit'
            url_namespace = 'edc-model-wrapper'
            next_url_name = 'listboard_url'
            next_url_attrs = ['v1', 'appointment']
            # querystring_attrs = ['f2', 'f3']

            @property
            def appointment(self):
                return self.object.appointment.id

        class AppointmentModelWrapper1(ModelWrapper):
            model = 'edc_model_wrapper.appointment'
            url_namespace = 'edc-model-wrapper'
            next_url_name = 'listboard_url'
            next_url_attrs = ['a1']
            # querystring_attrs = ['f2', 'f3']

            @property
            def visit(self):
                try:
                    model_obj = self.object.subjectvisit
                except ObjectDoesNotExist:
                    model_obj = SubjectVisit(
                        appointment=Appointment(a1=1), v1=1)
                return SubjectVisitModelWrapper1(model_obj=model_obj)

        class AppointmentModelWrapper2(ModelWrapper):
            model = 'edc_model_wrapper.appointment'
            url_namespace = 'edc-model-wrapper'
            next_url_name = 'listboard_url'
            next_url_attrs = ['a1']
            # querystring_attrs = ['f2', 'f3']

            @property
            def visit(self):
                try:
                    model_obj = self.object.subjectvisit
                except ObjectDoesNotExist:
                    model_obj = SubjectVisit(
                        appointment=Appointment(a1=1), v1=1)
                return SubjectVisitModelWrapper2(model_obj=model_obj)

        self.appointment_model_wrapper1_cls = AppointmentModelWrapper1
        self.appointment_model_wrapper2_cls = AppointmentModelWrapper2
        self.subject_visit_model_wrapper1_cls = SubjectVisitModelWrapper1
        self.subject_visit_model_wrapper2_cls = SubjectVisitModelWrapper2

    def test_wrapper(self):

        model_obj = Appointment.objects.create()
        self.appointment_model_wrapper1_cls(model_obj=model_obj)

    def test_wrapper_visit(self):
        model_obj = Appointment.objects.create()
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        self.assertIsNotNone(wrapper.visit)

    def test_wrapper_appointment_href(self):
        model_obj = Appointment.objects.create(a1=1)
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        self.assertIn(
            'next=edc-model-wrapper:listboard_url,a1&a1=1', wrapper.href)

    def test_wrapper_visit_href(self):
        model_obj = Appointment.objects.create(a1=1)
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        self.assertIn(
            'next=edc-model-wrapper:listboard_url,v1&v1=1', wrapper.visit.href)

    def test_wrapper_visit_href_persisted(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        self.assertIn(
            'next=edc-model-wrapper:listboard_url,v1&v1=2', wrapper.visit.href)

    def test_wrapper_visit_appointment_raises(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        try:
            wrapper.visit.appointment
        except AttributeError:
            pass
        else:
            self.fail('AttributeError unexpectedly not raised')

    def test_wrapper_visit_appointment_from_object(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        try:
            wrapper.visit.object.appointment
        except AttributeError:
            self.fail('AttributeError unexpectedly raised')

    def test_wrapper_visit_appointment_raises1(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper2_cls(model_obj=model_obj)
        try:
            wrapper.visit.appointment
        except AttributeError:
            self.fail('AttributeError unexpectedly raised')

    def test_wrapper_visit_href_with_appointment(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper2_cls(model_obj=model_obj)
        self.assertIn(
            f'next=edc-model-wrapper:listboard_url,v1,appointment&v1=2&appointment={model_obj.pk}',
            wrapper.visit.href)

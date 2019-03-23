from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag  # noqa

from ...wrappers import (
    ModelWrapper,
    ModelWrapperObjectAlreadyWrapped,
    ModelWrapperModelError,
)
from ..models import Example, Appointment, SubjectVisit, ParentExample


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectVisit)
class SubjectVisitAdmin(admin.ModelAdmin):
    pass


class TestModelWrapper(TestCase):
    def test_model_wrapper(self):
        """Asserts can construct.
        """
        obj = Example()
        ModelWrapper(model_obj=obj, model_cls=Example, next_url_name="thenexturl")

    def test_model_wrapper_assumes_model_cls(self):
        """Asserts can construct.
        """
        obj = Example()
        wrapper = ModelWrapper(model_obj=obj, next_url_name="thenexturl")
        self.assertEqual(wrapper.model_cls, Example)

    def test_model_wrapper_raises_on_wrong_model_cls(self):
        """Asserts can construct.
        """
        obj = Example()
        self.assertRaises(
            ModelWrapperModelError,
            ModelWrapper,
            model_obj=obj,
            model_cls=ParentExample,
            next_url_name="thenexturl",
        )

    def test_model_wrapper_raises_on_wrong_model_cls2(self):
        """Asserts can construct.
        """
        obj = Example()
        self.assertRaises(
            ModelWrapperModelError,
            ModelWrapper,
            model_obj=obj,
            model_cls=ParentExample,
            next_url_name="thenexturl",
        )

    def test_model_wrapper_raises_on_wrong_model_not_string(self):
        """Asserts can construct.
        """
        obj = Example()
        self.assertRaises(
            ModelWrapperModelError,
            ModelWrapper,
            model_obj=obj,
            model=ParentExample,
            next_url_name="thenexturl",
        )

    def test_model_wrapper_adds_kwargs_to_self(self):
        obj = Example()
        wrapper = ModelWrapper(model_obj=obj, next_url_name="thenexturl", erik="silly")
        self.assertEqual(wrapper.erik, "silly")

    def test_model_wrapper_bool(self):
        """Asserts wrapper can be truth tested.

        If model is not persisted is False.
        """
        obj = Example()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        self.assertIsNone(wrapper.object.id)
        self.assertFalse(bool(wrapper))

    def test_model_wrapper_bool2(self):
        """Asserts wrapper can be truth tested.

        If model is persisted is True.
        """
        obj = Example.objects.create()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        self.assertTrue(bool(wrapper))

    def test_model_wrapper_meta(self):
        """Asserts wrapper maintains _meta.
        """
        obj = Example.objects.create()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        self.assertEqual(wrapper._meta.label_lower, "edc_model_wrapper.example")

    def test_model_wrapper_repr(self):
        """Asserts wrapper maintains _meta.
        """
        obj = Example.objects.create()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        self.assertTrue(repr(wrapper))

    def test_model_wrapper_wraps_once(self):
        """Asserts a wrapped model instance cannot be wrapped.
        """
        obj = Example()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        obj = wrapper.object
        self.assertRaises(
            ModelWrapperObjectAlreadyWrapped,
            ModelWrapper,
            model_obj=obj,
            model_cls=Example,
            next_url_name="thenexturl",
        )

    def test_model_wrapper_invalid_name_raises(self):
        """Asserts raises if model does not match model instance.
        """
        ModelWrapper(
            model_obj=Example(),
            model="edc_model_wrapper.example",
            next_url_name="thenexturl",
        )
        self.assertRaises(
            ModelWrapperModelError,
            ModelWrapper,
            model_obj=Example(),
            model="blah",
            next_url_name="thenexturl",
        )

    def test_model_wrapper_model_is_class1(self):
        """Asserts model returns as a class if passed label_lower.
        """
        wrapper = ModelWrapper(
            model_obj=Example(),
            model="edc_model_wrapper.example",
            next_url_name="thenexturl",
        )
        self.assertEqual(wrapper.model_cls, Example)
        self.assertEqual(wrapper.model, Example._meta.label_lower)

    def test_model_wrapper_model_is_class2(self):
        """Asserts model returns as a class if passed class.
        """
        wrapper = ModelWrapper(
            model_obj=Example(), model_cls=Example, next_url_name="thenexturl"
        )
        self.assertEqual(wrapper.model_cls, Example)
        self.assertEqual(wrapper.model, Example._meta.label_lower)


class TestExampleWrappers(TestCase):
    def setUp(self):
        class ExampleModelWrapper(ModelWrapper):
            model = "edc_model_wrapper.example"
            next_url_name = "listboard_url"
            next_url_attrs = ["f1"]
            querystring_attrs = ["f2", "f3"]

        self.wrapper_cls = ExampleModelWrapper

    def test_model_wrapper_model_object(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(wrapper.object, model_obj)

    def test_model_wrapper_model_querystring(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(wrapper.querystring, "f2=2&f3=3")

    def test_model_wrapper_model_next_url(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertTrue(
            wrapper.href.split("next=")[1].startswith(
                "edc_model_wrapper:listboard_url,f1&f1=1"
            )
        )

    def test_example_href_add(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.href,
            "/admin/edc_model_wrapper/example/add/?next=edc_model_wrapper:listboard_url,"
            "f1&f1=1&f2=2&f3=3",
        )

    def test_example_href_change(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.href,
            f"/admin/edc_model_wrapper/example/{model_obj.pk}/change/?next=edc_model_"
            "wrapper:listboard_url,f1&f1=1&f2=2&f3=3",
        )

    def test_model_wrapper_admin_urls_add(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.admin_url_name,
            "edc_model_wrapper_admin:edc_model_wrapper_example_add",
        )

    def test_model_wrapper_admin_urls_change(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.admin_url_name,
            "edc_model_wrapper_admin:edc_model_wrapper_example_change",
        )

    def test_model_wrapper_history_url(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.history_url,
            f"/admin/edc_model_wrapper/example/{str(model_obj.id)}/history/",
        )

    def test_model_wrapper_fields(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertIsNotNone(wrapper.f1)
        self.assertIsNotNone(wrapper.f2)
        self.assertIsNotNone(wrapper.f3)
        self.assertIsNotNone(wrapper.revision)
        self.assertIsNotNone(wrapper.hostname_created)
        self.assertIsNotNone(wrapper.hostname_modified)
        self.assertIsNotNone(wrapper.user_created)
        self.assertIsNotNone(wrapper.user_modified)
        self.assertIsNotNone(wrapper.created)
        self.assertIsNotNone(wrapper.modified)


class TestExampleWrappers2(TestCase):
    """A group of tests that show a common scenario of
    Appointment and SubjectVisit.
    """

    def setUp(self):
        class SubjectVisitModelWrapper1(ModelWrapper):
            model = "edc_model_wrapper.subjectvisit"
            next_url_name = "listboard_url"
            next_url_attrs = ["v1"]
            # querystring_attrs = ['f2', 'f3']

        class SubjectVisitModelWrapper2(ModelWrapper):
            model = "edc_model_wrapper.subjectvisit"
            next_url_name = "listboard_url"
            next_url_attrs = ["v1", "appointment"]
            # querystring_attrs = ['f2', 'f3']

            @property
            def appointment(self):
                return self.object.appointment.id

        class AppointmentModelWrapper1(ModelWrapper):
            model = "edc_model_wrapper.appointment"
            next_url_name = "listboard_url"
            next_url_attrs = ["a1"]
            # querystring_attrs = ['f2', 'f3']

            @property
            def visit(self):
                try:
                    model_obj = self.object.subjectvisit
                except ObjectDoesNotExist:
                    model_obj = SubjectVisit(appointment=Appointment(a1=1), v1=1)
                return SubjectVisitModelWrapper1(model_obj=model_obj)

        class AppointmentModelWrapper2(ModelWrapper):
            model = "edc_model_wrapper.appointment"
            next_url_name = "listboard_url"
            next_url_attrs = ["a1"]
            # querystring_attrs = ['f2', 'f3']

            @property
            def visit(self):
                model_obj = self.object.subjectvisit
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
        self.assertIn("next=edc_model_wrapper:listboard_url,a1&a1=1", wrapper.href)

    def test_wrapper_visit_href(self):
        model_obj = Appointment.objects.create(a1=1)
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        self.assertIn(
            "next=edc_model_wrapper:listboard_url,v1&v1=1", wrapper.visit.href
        )

    def test_wrapper_visit_href_persisted(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        self.assertIn(
            "next=edc_model_wrapper:listboard_url,v1&v1=2", wrapper.visit.href
        )

    def test_wrapper_visit_appointment_raises(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        try:
            wrapper.visit.appointment
        except AttributeError:
            pass
        else:
            self.fail("AttributeError unexpectedly not raised")

    def test_wrapper_visit_appointment_from_object(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper1_cls(model_obj=model_obj)
        try:
            wrapper.visit.object.appointment
        except AttributeError:
            self.fail("AttributeError unexpectedly raised")

    def test_wrapper_visit_appointment_raises1(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper2_cls(model_obj=model_obj)
        try:
            wrapper.visit.appointment
        except AttributeError:
            self.fail("AttributeError unexpectedly raised")

    def test_wrapper_visit_href_with_appointment(self):
        model_obj = Appointment.objects.create(a1=1)
        SubjectVisit.objects.create(appointment=model_obj, v1=2)
        wrapper = self.appointment_model_wrapper2_cls(model_obj=model_obj)
        self.assertIn(
            f"next=edc_model_wrapper:listboard_url,v1,appointment&v1=2&appointment={model_obj.pk}",
            wrapper.visit.href,
        )

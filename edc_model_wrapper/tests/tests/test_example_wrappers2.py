from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag  # noqa

from ...wrappers import ModelWrapper
from ..models import Appointment, SubjectVisit


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

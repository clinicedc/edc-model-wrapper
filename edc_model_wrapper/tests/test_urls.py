from django.test import TestCase, tag
from django.views.generic.base import TemplateView

from ..url_mixins import NextUrlMixin


class TestUrls(TestCase):

    def test_next_url(self):
        view = NextUrlMixin()
        view.kwargs = {}
        self.assertEqual(view.get_next_url(), '')

    def test_next_url_add_paramters_no_values(self):
        """Assert if values not in kwargs parameters are removed."""
        class Dummy(NextUrlMixin, TemplateView):
            @property
            def next_url_parameters(self):
                parameters = super().next_url_parameters
                parameters.update({
                    'appointment': ['subject_identifier', 'selected_obj'],
                    'visit': ['subject_identifier', 'appointment']})
                return parameters
        view = Dummy()
        view.kwargs = {}
        options = {}
        self.assertEqual(view.get_next_url(**options), '')

    def test_next_url_add_paramters_with_values(self):
        """Assert if values in kwargs parameters are not removed."""
        class Dummy(NextUrlMixin, TemplateView):
            @property
            def next_url_parameters(self):
                parameters = super().next_url_parameters
                parameters.update({
                    'appointment': ['subject_identifier', 'selected_obj'],
                    'visit': ['subject_identifier', 'appointment']})
                return parameters
        view = Dummy()
        view.kwargs = {'subject_identifier': '123456-0'}
        self.assertEqual(
            view.get_next_url('appointment'),
            'dashboard_url,subject_identifier&subject_identifier=123456-0')

    def test_next_url_add_paramters_with_values_ignores_others(self):
        class Dummy(NextUrlMixin, TemplateView):
            @property
            def next_url_parameters(self):
                parameters = super().next_url_parameters
                parameters.update({
                    'appointment': ['subject_identifier', 'selected_obj'],
                    'visit': ['subject_identifier', 'appointment']})
                return parameters
        view = Dummy()
        view.kwargs = {'subject_identifier': '123456-0'}
        options = {'some_value': 'abcdef'}
        self.assertEqual(
            view.get_next_url('appointment', **options),
            'dashboard_url,subject_identifier&subject_identifier=123456-0')

from datetime import timedelta
from django.test import TestCase, tag

from edc_base.utils import get_utcnow

from ..wrappers import ModelWrapper, ModelWithLogWrapper
from .models import Example, ExampleLog, ExampleLogEntry
from edc_model_wrapper.tests.models import UnrelatedExample


class ExampleModelWrapper(ModelWrapper):
    model = 'edc_model_wrapper.example'
    url_namespace = 'edc-model-wrapper'
    next_url_name = 'listboard_url'
    next_url_attrs = ['f1']
    querystring_attrs = ['f2', 'f3']


class ParentExampleModelWrapper(ModelWrapper):

    model_name = 'edc_model_wrapper.parentexample'
    next_url_attrs = ['f1']
    querystring_attrs = ['f2', 'f3']
    url_attrs = ['f1', 'f2', 'f3']
    url_namespace = 'edc-model-wrapper'


class ExampleLogEntryModelWrapper(ModelWrapper):

    model_name = 'edc_model_wrapper.examplelogentry'
    next_url_attrs = ['example_identifier', 'example_log']
    querystring_attrs = ['f2', 'f3']
    url_attrs = ['example_identifier', 'example_log']
    url_namespace = 'edc-model-wrapper'

    @property
    def example_identifier(self):
        return self._original_object.example_log.example.example_identifier

    @property
    def survey(self):
        return 'survey_one'


class ParentExampleModelWithLogWrapper(ModelWithLogWrapper):

    model_wrapper_class = ParentExampleModelWrapper
    log_entry_model_wrapper_class = ExampleLogEntryModelWrapper

    parent_model_wrapper_class = ExampleModelWrapper
    parent_lookup = 'example'


class TestModelWithLogWrapper(TestCase):

    def test_wrapper_object(self):
        example = Example.objects.create()
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(wrapper.object, example)

    def test_wrapper_log(self):
        example = Example.objects.create()
        log = ExampleLog.objects.create(example=example)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(wrapper.log.object.example, log.example)

    def test_wrapper_log_entry(self):
        example = Example.objects.create()
        log = ExampleLog.objects.create(example=example)
        log_entry = ExampleLogEntry.objects.create(example_log=log)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(
            wrapper.log_entry.object.example_log,
            log_entry.example_log)

    def test_wrapper_fills_log_entry(self):
        """Asserts adds a non-persisted instance of log entry
        if a persisted one does not exist.
        """
        example = Example.objects.create()
        example_log = ExampleLog.objects.create(example=example)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertIsNone(wrapper.log_entry.object.id)
        self.assertEqual(
            example_log,
            wrapper.log_entry.object.example_log)

    def test_wrapper_fills_log(self):
        """Asserts adds a non-persisted instance of log
        if a persisted one does not exist.
        """
        example = Example.objects.create()
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertIsNone(wrapper.log.object.id)
        self.assertEqual(example, wrapper.log.object.example)

    def test_wrapper_fills_log_and_logentry(self):
        """Asserts adds a non-persisted instance of log and log entry
        if a persisted ones do not exist.
        """
        example = Example.objects.create()
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertIsNone(wrapper.log.object.id)
        self.assertIsNone(wrapper.log_entry.object.id)

    def test_wrapper_no_entries(self):
        example = Example.objects.create()
        ExampleLog.objects.create(example=example)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(wrapper.log_entries, [])

    def test_wrapper_multpile_log_entries(self):
        example = Example.objects.create()
        example_log = ExampleLog.objects.create(example=example)
        ExampleLogEntry.objects.create(example_log=example_log)
        ExampleLogEntry.objects.create(example_log=example_log)
        ExampleLogEntry.objects.create(example_log=example_log)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(len(wrapper.log_entries), 3)

    def test_wrapper_picks_first_log_entry(self):
        example = Example.objects.create()
        example_log = ExampleLog.objects.create(example=example)
        report_datetime = get_utcnow() - timedelta(days=1)
        ExampleLogEntry.objects.create(
            example_log=example_log,
            report_datetime=get_utcnow() - timedelta(days=3))
        ExampleLogEntry.objects.create(
            example_log=example_log,
            report_datetime=get_utcnow() - timedelta(days=2))
        ExampleLogEntry.objects.create(
            example_log=example_log,
            report_datetime=report_datetime)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(
            wrapper.log_entry.object.report_datetime, report_datetime)


class TestModelWithLogWrapperUrls(TestCase):

    @tag('5')
    def test_unrelated_wrapper_log(self):
        example = Example.objects.create()
        uexample = UnrelatedExample.objects.create()
        log = ExampleLog.objects.create(example=example)
        wrapper = ModelWithLogWrapper(
            model_obj=uexample, next_url_name='listboard', lookup='example')
        self.assertEqual(wrapper.log.object.unexample, log.example)

    @tag('2')
    def test_wrapper_urls(self):
        example = Example.objects.create()
        example_log = ExampleLog.objects.create(example=example)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertIn(
            f'example_log={example_log.id}',
            wrapper.log_entry.next_url)
        self.assertIn(
            'listboard_url',
            wrapper.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_log',
            wrapper.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier',
            wrapper.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier={}'.format(self.example.example_identifier),
            wrapper.log_entry.next_url)

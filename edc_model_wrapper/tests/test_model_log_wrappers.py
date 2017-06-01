from datetime import timedelta
from django.test import TestCase, tag

from edc_base.utils import get_utcnow

from ..wrappers import ModelWrapper, ModelWithLogWrapper
from .models import Example, ParentExample, ExampleLog, ExampleLogEntry


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

    @tag('1')
    def test_wrapper_determines_relations(self):
        pass

    @tag('1')
    def test_wrapper_object(self):
        example = Example.objects.create()
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(wrapper.object, example)

    @tag('1')
    def test_wrapper_log(self):
        example = Example.objects.create()
        log = ExampleLog.objects.create(example=example)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(wrapper.log.object.example, log.example)

    @tag('1')
    def test_wrapper_log_entry(self):
        example = Example.objects.create()
        log = ExampleLog.objects.create(example=example)
        log_entry = ExampleLogEntry.objects.create(example_log=log)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(
            wrapper.log_entry.object.example_log,
            log_entry.example_log)

    @tag('1')
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

    @tag('1')
    def test_wrapper_fills_log(self):
        """Asserts adds a non-persisted instance of log
        if a persisted one does not exist.
        """
        example = Example.objects.create()
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertIsNone(wrapper.log.object.id)
        self.assertEqual(example, wrapper.log.object.example)

    @tag('1')
    def test_wrapper_fills_log_and_logentry(self):
        """Asserts adds a non-persisted instance of log and log entry
        if a persisted ones do not exist.
        """
        example = Example.objects.create()
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertIsNone(wrapper.log.object.id)
        self.assertIsNone(wrapper.log_entry.object.id)

    @tag('1')
    def test_wrapper_no_entries(self):
        example = Example.objects.create()
        ExampleLog.objects.create(example=example)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(wrapper.log_entries, [])

    @tag('1')
    def test_wrapper_multpile_log_entries(self):
        example = Example.objects.create()
        example_log = ExampleLog.objects.create(example=example)
        ExampleLogEntry.objects.create(example_log=example_log)
        ExampleLogEntry.objects.create(example_log=example_log)
        ExampleLogEntry.objects.create(example_log=example_log)
        wrapper = ModelWithLogWrapper(
            model_obj=example, next_url_name='listboard')
        self.assertEqual(len(wrapper.log_entries), 3)

    @tag('1')
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


class TestModelWithLogWrapper2(TestCase):

    def setUp(self):

        class ExampleModelWithLogWrapper(ModelWithLogWrapper):

            model_wrapper_class = ExampleModelWrapper
            log_entry_model_wrapper_cls = ExampleLogEntryModelWrapper

        self.model_log_wrapper_cls = ExampleModelWithLogWrapper

        self.example = Example.objects.create(
            example_identifier='123456-0', f1=5, f2=6)
        self.parent_example = ParentExample.objects.create(
            example=self.example)
        self.example_log = ExampleLog.objects.create(example=self.example)
        ExampleLogEntry.objects.create(example_log=self.example_log)
        ExampleLogEntry.objects.create(example_log=self.example_log)
        ExampleLogEntry.objects.create(example_log=self.example_log)
        self.example = Example.objects.get(id=self.example.id)

    def test_wrapper(self):
        self.wrapper = self.model_log_wrapper_cls(self.example)

    def test_object_without_log(self):
        self.example.examplelog.delete()
        self.example = Example.objects.get(id=self.example.id)
        self.wrapped_object = ExampleModelWithLogWrapper(self.example)
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)

    def test_object_with_log_only(self):
        self.example.examplelog.examplelogentry_set.all().delete()
        self.example = Example.objects.get(id=self.example.id)
        self.wrapped_object = ExampleModelWithLogWrapper(self.example)
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)
        self.assertIsNotNone(self.wrapped_object.log)
        self.assertIsNotNone(self.wrapped_object.log_entry)
        self.assertTrue(self.wrapped_object.log_entry._mocked_object)

    def test_object_with_log_entry(self):
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)
        self.assertIsNotNone(self.wrapped_object.log)
        self.assertIsNotNone(self.wrapped_object.log_entry)
        self.assertTrue(self.wrapped_object.log_entry._mocked_object)

    def test_object_with_current_log_entry(self):
        self.wrapped_object = ExampleModelWithLogWrapper(
            self.example, report_datetime=get_utcnow())
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)
        self.assertIsNotNone(self.wrapped_object.log)
        self.assertIsNotNone(self.wrapped_object.log_entry)
        try:
            self.wrapped_object.log_entry._mocked_object
            self.fail('Unexpected got a mocked log entry object')
        except AttributeError:
            pass

        self.assertIn(
            'example_log={}'.format(self.example.examplelog.id),
            self.wrapped_object.log_entry.next_url)

        self.assertIn(
            'listboard_url',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_log',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier={}'.format(self.example.example_identifier),
            self.wrapped_object.log_entry.next_url)

    def test_object_with_different_parent_and_model(self):
        self.wrapped_object = ParentExampleModelWithLogWrapper(
            self.parent_example, report_datetime=get_utcnow())
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)
        self.assertIsNotNone(self.wrapped_object.log)
        self.assertIsNotNone(self.wrapped_object.log_entry)
        self.assertIsNotNone(self.wrapped_object.parent)
        self.assertEqual(self.wrapped_object.parent.id,
                         str(self.parent_example.example.id))
        try:
            self.wrapped_object.log_entry._mocked_object
            self.fail('Unexpected got a mocked log entry object')
        except AttributeError:
            pass

        self.assertIn(
            'example_log={}'.format(self.example.examplelog.id),
            self.wrapped_object.log_entry.next_url)

        self.assertIn(
            'listboard_url',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_log',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier={}'.format(self.example.example_identifier),
            self.wrapped_object.log_entry.next_url)

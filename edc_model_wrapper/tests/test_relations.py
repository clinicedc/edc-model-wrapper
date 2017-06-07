from django.test import TestCase, tag

from ..wrappers import ModelRelation
from .models import Example, ExampleLog, ExampleLogEntry


class TestModelRealtions(TestCase):

    def setUp(self):
        self.example = Example.objects.create()
        self.example_log = ExampleLog.objects.create(example=self.example)
        self.example_log_entry = ExampleLogEntry.objects.create(
            example_log=self.example_log)

    def test_model_relations_by_schema(self):
        model_relations = ModelRelation(
            model_obj=self.example,
            schema=['example', 'example_log', 'example_log_entry'])
        self.assertEqual(model_relations.log_model, ExampleLog)
        self.assertEqual(model_relations.log_entry_model, ExampleLogEntry)

    def test_model_relations_by_schema2(self):
        model_relations = ModelRelation(
            model_obj=self.example,
            schema=['example', 'example_log', 'example_log_entry'])
        self.assertIsInstance(model_relations.log, ExampleLog)
        self.assertIsInstance(model_relations.log_entry, ExampleLogEntry)

    def test_model_relations_by_schema3(self):
        model_relations = ModelRelation(
            model_obj=self.example,
            schema=['example', 'edc_model_wrapper.example_log', 'edc_model_wrapper.example_log_entry'])
        self.assertIsInstance(model_relations.log, ExampleLog)
        self.assertIsInstance(model_relations.log_entry, ExampleLogEntry)

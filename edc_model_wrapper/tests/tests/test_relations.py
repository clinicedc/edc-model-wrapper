from django.test import TestCase, tag

from ...wrappers import ModelRelation, LogModelRelation
from ..models import (
    Example,
    ExampleLog,
    ExampleLogEntry,
    ParentExample,
    SuperParentExample,
)


class TestModelRelations(TestCase):
    def setUp(self):
        self.example = Example.objects.create()
        self.example_log = ExampleLog.objects.create(example=self.example)
        self.example_log_entry = ExampleLogEntry.objects.create(
            example_log=self.example_log
        )

    def test_model_relations_by_schema(self):
        model_relations = ModelRelation(
            model_obj=self.example,
            schema=["example", "example_log", "example_log_entry"],
        )
        self.assertEqual(model_relations.log_model, ExampleLog)
        self.assertEqual(model_relations.log_entry_model, ExampleLogEntry)

    def test_model_relations_by_schema2(self):
        model_relations = ModelRelation(
            model_obj=self.example,
            schema=["example", "example_log", "example_log_entry"],
        )
        self.assertIsInstance(model_relations.log, ExampleLog)
        self.assertIsInstance(model_relations.log_entry, ExampleLogEntry)


class TestLogModelRelations(TestCase):
    def setUp(self):
        self.example_identifier = "12345"
        self.example = Example.objects.create(
            example_identifier=self.example_identifier
        )
        self.parent_example = ParentExample.objects.create(example=self.example)
        self.super_parent_example = SuperParentExample.objects.create(
            parent_example=self.parent_example
        )
        self.example_log = ExampleLog.objects.create(example=self.example)
        self.example_log_entry = ExampleLogEntry.objects.create(
            example_log=self.example_log
        )

    @tag("2")
    def test_log_model_relations(self):
        model_relations = LogModelRelation(model_obj=self.example)
        self.assertEqual(model_relations.log_model, ExampleLog)
        self.assertEqual(model_relations.log_entry_model, ExampleLogEntry)

    def test_log_model_relations1(self):
        model_relations = LogModelRelation(
            model_obj=self.example,
            log_model_name="example_log",
            log_entry_model_name="example_log_entry",
        )
        self.assertEqual(model_relations.log_model, ExampleLog)
        self.assertEqual(model_relations.log_entry_model, ExampleLogEntry)

    @tag("2")
    def test_log_model_relations2(self):
        model_relations = LogModelRelation(
            model_obj=self.parent_example, related_lookup="example"
        )
        self.assertEqual(model_relations.log_model, ExampleLog)
        self.assertEqual(model_relations.log_entry_model, ExampleLogEntry)

    def test_log_model_relations3(self):
        model_relations = LogModelRelation(
            model_obj=self.parent_example,
            related_lookup="example",
            log_model_name="example_log",
            log_entry_model_name="example_log_entry",
        )
        self.assertEqual(model_relations.log_model, ExampleLog)
        self.assertEqual(model_relations.log_entry_model, ExampleLogEntry)

    @tag("2")
    def test_log_model_relations4(self):
        model_relations = LogModelRelation(
            model_obj=self.super_parent_example,
            related_lookup="parent_example__example",
        )
        self.assertEqual(model_relations.log_model, ExampleLog)
        self.assertEqual(model_relations.log_entry_model, ExampleLogEntry)

    def test_log_model_relations5(self):
        model_relations = LogModelRelation(
            model_obj=self.super_parent_example,
            related_lookup="parent_example__example",
            log_model_name="example_log",
            log_entry_model_name="example_log_entry",
        )
        self.assertEqual(model_relations.log_model, ExampleLog)
        self.assertEqual(model_relations.log_entry_model, ExampleLogEntry)

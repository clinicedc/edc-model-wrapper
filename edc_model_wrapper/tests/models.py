__all__ = ['Example', 'ParentExample', 'ExampleLog', 'ExampleLogEntry']

import uuid

from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow


class Example(BaseUuidModel):

    example_identifier = models.CharField(
        max_length=10, unique=True)

    f1 = models.CharField(max_length=10)

    f2 = models.CharField(max_length=10, null=True)

    f3 = models.CharField(max_length=10, default=uuid.uuid4())

    report_datetime = models.DateTimeField(
        default=get_utcnow)


class UnrelatedExample(BaseUuidModel):

    example_identifier = models.CharField(
        max_length=10, unique=True)

    f1 = models.CharField(max_length=10)

    f2 = models.CharField(max_length=10, null=True)

    f3 = models.CharField(max_length=10, default=uuid.uuid4())

    report_datetime = models.DateTimeField(
        default=get_utcnow)


class ParentExample(BaseUuidModel):

    f1 = models.CharField(max_length=10)

    f2 = models.CharField(max_length=10, null=True)

    f3 = models.CharField(max_length=10, default=uuid.uuid4())

    example = models.ForeignKey(Example)

    report_datetime = models.DateTimeField(
        default=get_utcnow)


class ExampleLog(BaseUuidModel):

    example = models.OneToOneField(Example)

    f1 = models.CharField(max_length=10, unique=True)

    report_datetime = models.DateTimeField(
        default=get_utcnow)


class ExampleLogEntry(BaseUuidModel):

    example_log = models.ForeignKey(ExampleLog)

    report_datetime = models.DateTimeField(
        default=get_utcnow)


class Appointment(BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    a1 = models.CharField(max_length=10)


class SubjectVisit(BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    v1 = models.CharField(max_length=10)

    appointment = models.OneToOneField(Appointment)

import uuid

from django.db import models
from django.db.models.deletion import PROTECT
from edc_model.models import BaseUuidModel
from edc_utils import get_utcnow


class Example(BaseUuidModel):

    example_identifier = models.CharField(max_length=10, unique=True)

    f1 = models.CharField(max_length=10)

    f2 = models.CharField(max_length=10, null=True)

    f3 = models.CharField(max_length=10, default=uuid.uuid4())

    report_datetime = models.DateTimeField(default=get_utcnow)


class UnrelatedExample(BaseUuidModel):

    example_identifier = models.CharField(max_length=10, unique=True)

    f1 = models.CharField(max_length=10)

    f2 = models.CharField(max_length=10, null=True)

    f3 = models.CharField(max_length=10, default=uuid.uuid4())

    report_datetime = models.DateTimeField(default=get_utcnow)


class ParentExample(BaseUuidModel):

    f1 = models.CharField(max_length=10)

    f2 = models.CharField(max_length=10, null=True)

    f3 = models.CharField(max_length=10, default=uuid.uuid4())

    example = models.ForeignKey(Example, null=True, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)


class SuperParentExample(BaseUuidModel):

    f1 = models.CharField(max_length=10)

    f2 = models.CharField(max_length=10, null=True)

    f3 = models.CharField(max_length=10, default=uuid.uuid4())

    parent_example = models.ForeignKey(ParentExample, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)


class ExampleLog(BaseUuidModel):

    example = models.OneToOneField(Example, on_delete=PROTECT)

    f1 = models.CharField(max_length=10, unique=True)

    report_datetime = models.DateTimeField(default=get_utcnow)


class ExampleLogEntry(BaseUuidModel):

    example_log = models.ForeignKey(ExampleLog, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)


class Appointment(BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    a1 = models.CharField(max_length=10)


class SubjectVisit(BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    v1 = models.CharField(max_length=10)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

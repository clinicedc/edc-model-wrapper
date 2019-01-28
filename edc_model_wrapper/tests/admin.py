from django.contrib import admin
from django.contrib.admin import AdminSite as DjangoAdminSite

from .models import Example, ExampleLog, ExampleLogEntry, SubjectVisit
from .models import ParentExample, Appointment


class AdminSite(DjangoAdminSite):
    site_title = "Example"
    site_header = "Example"
    index_title = "Example"
    site_url = "/"


edc_model_wrapper_admin = AdminSite(name="edc_model_wrapper_admin")


@admin.register(Example, site=edc_model_wrapper_admin)
class ExampleAdmin(admin.ModelAdmin):
    pass


@admin.register(ExampleLog, site=edc_model_wrapper_admin)
class ExampleLogAdmin(admin.ModelAdmin):
    pass


@admin.register(ExampleLogEntry, site=edc_model_wrapper_admin)
class ExampleLogEntryAdmin(admin.ModelAdmin):
    pass


@admin.register(ParentExample, site=edc_model_wrapper_admin)
class ParentExampleAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectVisit, site=edc_model_wrapper_admin)
class SubjectVisitAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment, site=edc_model_wrapper_admin)
class AppointmentAdmin(admin.ModelAdmin):
    pass

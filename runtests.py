#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from os.path import abspath, dirname


app_name = 'edc_model_wrapper'
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    template_dirs=[os.path.join(
        base_dir, app_name, "tests", "templates")],
    APP_NAME=app_name,
    BASE_DIR=base_dir,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    DATABASES={
        # required for tests when acting as a server that deserializes
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(base_dir, 'db.sqlite3'),
        },
        'client': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(base_dir, 'db.sqlite3'),
        },
    },
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "edc_model_wrapper.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
    use_test_urls=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split('=')[1] for t in sys.argv if t.startswith('--tag')]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests(
        [f'{app_name}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()

import sys

if 'test' in sys.argv:
    from .tests.models import Example, ParentExample, SuperParentExample, UnrelatedExample, ExampleLog, ExampleLogEntry

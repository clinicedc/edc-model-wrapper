import sys

if 'test' in sys.argv:
    from .tests.models import Example, ParentExample, SuperParentExample
    from .tests.models import UnrelatedExample, ExampleLog, ExampleLogEntry

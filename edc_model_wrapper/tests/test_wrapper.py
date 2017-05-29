from django.test import TestCase, tag

from ..wrapper import Wrapper
from .models import Example


@tag('w')
class TestWrapper(TestCase):

    def test_wrapper(self):
        example = Example(f1=1, f2=2)
        wrapper = Wrapper(example)
        self.assertTrue(wrapper._wrapped)

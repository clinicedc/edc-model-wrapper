from urllib import parse

from .keywords import Keywords
from pprint import pprint


class NextUrlError(Exception):
    pass


class NextUrlParser:

    """A class to set `next_url`.

    `next_url` is  a qyerystring that follows the format of edc_base model
        admin mixin for redirecting the model admin on save
        to a url other than the default changelist.
        * Note: This is not a url but parameters need to reverse
                to one in the template.

    User is responsible for making sure the url_name can be reversed
    with the given parameters.

    In your url &next=my_url_name,arg1,arg2&agr1=value1&arg2=
    value2&arg3=value3&arg4=value4...etc.

    * next_url_attrs:
        A dict with a list of querystring attrs to include in the next url.

        Format is:
            {key1: [param1, param2, ...], key2: [param1, param2, ...]}

    """
    keywords_cls = Keywords

    def __init__(self, url_name=None, url_args=None, url_namespace=None, **kwargs):
        if not url_name:
            raise NextUrlError(f'Invalid url_name. Got {url_name}')
        self.url_name = url_name
        self.url_args = url_args
        self.url_namespace = url_namespace

    def querystring(self, objects=None, **kwargs):
        """Returns a querystring or ''.

            objects: a list of objects to from which to get attr values.
        """
        if self.url_args:
            url_namespace = f'{self.url_namespace}:' if self.url_namespace else ''
            next_args = ',{}'.format(','.join(self.url_args))
            url_kwargs = {
                k: v for k, v in kwargs.items() if k in (self.url_args or [])}
            keywords = self.keywords_cls(
                objects=objects, attrs=self.url_args, include_attrs=self.url_args, **url_kwargs)
            querystring = parse.urlencode(keywords, encoding='utf-8')
            return f'{url_namespace}{self.url_name}{next_args}&{querystring}'
        return ''

#     def reverse(self):
#         return reverse(self.url_name, kwargs=self._next_kwargs)

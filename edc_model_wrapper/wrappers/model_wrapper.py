from django.apps import apps as django_apps
from urllib import parse

from ..parsers import NextUrlParser, Keywords
from .fields import Fields


class ModelWrapperError(Exception):
    pass


class ModelWrapperModelError(Exception):
    pass


class ModelWrapperObjectAlreadyWrapped(Exception):
    pass


class ModelWrapperInvalidProperty(Exception):
    pass


class ModelWrapper:

    """A wrapper for model instances or classes.

    Keyword args:
        model_obj: An instance of a model class
        model_name: name of model class that wrapper accepts,
            if specified. (Default: None)

    Set attrs, flatten relations, adds admin and next urls,
    onto a model object to be used in views and templates.

    Common model and url attrs are added onto self so you can avoid
    accessing the model instance directly.
    For example:
        instead of this:
            model_wrapper.object.created  # not allowed in templates
            model_wrapper.wrapped_object.created
            model_wrapper.<my model name>.created
        this:
            model_wrapper.created

    * object: The wrapped model instance. Will include URLs
        and any other attrs that the wrapper is configured to add.
    * """

    fields_cls = Fields
    keywords_cls = Keywords
    next_url_parser_cls = NextUrlParser

    model = None  # class or label_lower
    url_namespace = None
    next_url_name = None
    next_url_attrs = []
    querystring_attrs = []

    def __init__(self, model_obj=None, model=None, next_url_name=None,
                 next_url_attrs=None, querystring_attrs=None,
                 url_namespace=None, **kwargs):

        self.object = model_obj
        self.model = model or self.model
        try:
            self.model = django_apps.get_model(*self.model.split('.'))
        except AttributeError:
            pass
        except ValueError as e:
            raise ModelWrapperModelError(f'{e}. Got model={model}.')

        self.fields = self.fields_cls(
            model_obj=self.object, model=self.model, **kwargs).fields

        self.url_namespace = url_namespace or self.url_namespace
        self.querystring_attrs = querystring_attrs or self.querystring_attrs
        self.next_url_parser = self.next_url_parser_cls(
            url_name=next_url_name or self.next_url_name,
            url_args=next_url_attrs or self.next_url_attrs,
            url_namespace=self.url_namespace,
            ** kwargs)
        # assert model obj can only be wrapped once.
        try:
            assert not self.object.wrapped
        except AttributeError:
            pass
        except AssertionError:
            raise ModelWrapperObjectAlreadyWrapped(
                f'Model is already wrapped. Got {self.object}')
        # ??
#         for key, value in self.__dict__.items():
#             if hasattr(value, 'wrapped'):
#                 raise ModelWrapperInvalidProperty(
#                     'Invalid property. Property may not return a wrapped object. '
#                     f'Got {key}, {value}')

        # wrap me with kwargs
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        # wrap me with field attrs
        for name, value in self.fields(wrapper=self):
            setattr(self, name, value)

        # wrap me with urls
        self.next_url = self.next_url_parser.querystring(
            objects=[self, self.object], **kwargs)
        self.get_absolute_url = self.object.get_absolute_url
        self.admin_url_name = f'{self.url_namespace}:{self.object.admin_url_name}'
        keywords = self.keywords_cls(
            objects=[self], attrs=self.querystring_attrs, **kwargs)
        self.querystring = parse.urlencode(keywords, encoding='utf-8')
        self.object.wrapped = True
        self.object.save = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.object} id={self.object.id})'

    def __bool__(self):
        return True if self.object.id else False

    def _meta(self):
        raise ModelWrapperError('This is not a model!')

    @classmethod
    def new(cls, **kwargs):
        model = django_apps.get_model(*cls.model_name.split('.'))
        return cls(model(), **kwargs)

    @property
    def href(self):
        return f'{self.get_absolute_url()}?{self.next_url}&{self.querystring}'

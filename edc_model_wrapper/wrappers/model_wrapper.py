from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_dashboard import url_names
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


class ModelWrapperNoReverseMatch(Exception):
    pass


class ModelWrapper:

    """A wrapper for model instances or classes.

    Keyword args:
        model_obj: An instance of a model class
        model: name of model class that wrapper accepts,
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

    model = None  # label_lower
    model_cls = None
    next_url_name = None  # should include namespace:url_name
    next_url_attrs = []
    querystring_attrs = []

    def __init__(
        self,
        model_obj=None,
        model=None,
        model_cls=None,
        next_url_name=None,
        next_url_attrs=None,
        querystring_attrs=None,
        force_wrap=None,
        **kwargs,
    ):

        self._href = None
        self._next_url = None
        self._next_url_name = next_url_name or self.next_url_name
        self.kwargs = kwargs

        self.object = model_obj
        if not force_wrap:
            self._raise_if_model_obj_is_wrapped()
        self.model_cls = model_cls or self.model_cls or self.object.__class__
        self.model_name = self.model_cls._meta.object_name.lower().replace(" ", "_")
        self.model = model or self.model or self.model_cls._meta.label_lower
        if not isinstance(self.object, self.model_cls):
            raise ModelWrapperModelError(
                f"Expected an instance of {self.model}. "
                f"Got model_obj={repr(self.object)}"
            )
        if self.model != self.model_cls._meta.label_lower:
            raise ModelWrapperModelError(
                f"Wrapper is for model {self.model}. "
                f"Got model_obj={repr(self.object)}. "
                f"{self.model} != {self.model_cls._meta.label_lower}."
            )

        fields_obj = self.fields_cls(model_obj=self.object)
        self.fields = fields_obj.get_field_values_as_strings

        self.next_url_attrs = next_url_attrs or self.next_url_attrs
        self.querystring_attrs = querystring_attrs or self.querystring_attrs

        self.wrap_me_with(self.kwargs)
        self.wrap_me_with({f[0]: f[1] for f in self.fields(wrapper=self)})

        # wrap me with admin urls
        self.get_absolute_url = self.object.get_absolute_url
        # see also UrlModelMixin.admin_url_name
        self.admin_url_name = f"{self.object.admin_url_name}"

        # wrap with an additional querystring for extra values needed
        # in the view
        self.keywords = self.keywords_cls(
            objects=[self], attrs=self.querystring_attrs, **self.kwargs
        )
        self.querystring = parse.urlencode(self.keywords, encoding="utf-8")

        # flag as wrapped and disable save
        self.object.wrapped = True
        self.object.save = None
        self.add_extra_attributes_after()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.object} id={self.object.id})"

    def __bool__(self):
        return True if self.object.id else False

    @property
    def href(self):
        # reverse admin url (must be registered w/ the site admin)
        if not self._href:
            # wrap me with next url and it's required attrs
            next_url = url_names.get(self.get_next_url_name())
            querystring = self.next_url_parser.querystring(
                objects=[self, self.object], **self.kwargs
            )
            if querystring:
                next_url = f"{next_url},{querystring}"
            self._href = f"{self.get_absolute_url()}?next={next_url}&{self.querystring}"
        return self._href

    def get_next_url_name(self):
        if not self._next_url_name:
            raise ModelWrapperError(
                f"'next_url_name' cannot be None. See {repr(self)}."
            )
        return self._next_url_name

    @property
    def next_url_parser(self):
        return self.next_url_parser_cls(
            url_name=self.get_next_url_name(), url_args=self.next_url_attrs
        )

    def wrap_me_with(self, dct):
        for key, value in dct.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                # skip if attr cannot be overwritten
                pass

    def reverse(self, model_wrapper=None):
        """Returns the reversed next_url_name or None.
        """
        try:
            next_url = self.next_url_parser.reverse(model_wrapper=model_wrapper or self)
        except NoReverseMatch as e:
            raise ModelWrapperNoReverseMatch(
                f"next_url_name={self.get_next_url_name()}. Got {e} {repr(self)}"
            )
        return next_url

    def add_extra_attributes_after(self, **kwargs):
        """Called after the model is wrapped.
        """
        pass

    @property
    def _meta(self):
        return self.object._meta

    def _raise_if_model_obj_is_wrapped(self):
        """Raises if the model instance is already wrapped.
        """
        try:
            assert not self.object.wrapped
        except AttributeError:
            pass
        except AssertionError:
            raise ModelWrapperObjectAlreadyWrapped(
                f"Model instance is already wrapped. "
                f"Got wrapped={self.object.wrapped}. See {repr(self)}"
            )

    @property
    def history_url(self):
        admin = self.admin_url_name.split(":")[0]
        if not self.object.id:
            return None
        return reverse(
            f"{admin}:{self.object._meta.app_label}_{self.object._meta.model_name}_history",
            args=(str(self.object.id),),
        )

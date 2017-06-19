from django.utils.text import camel_case_to_spaces

from .fields import Fields
from .model_relation import LogModelRelation
from .model_wrapper import ModelWrapper


class ModelWithLogWrapperError(Exception):
    pass


class ModelWithLogWrapper:

    """A model wrapper that expects the given model instance to
    follow the LogEntry relational schema.

    For example:
        Plot->PlotLog->PlotLogEntry where Plot is the model that the
        class is instantiated with.
    """

    fields_cls = Fields
    model_relation_cls = LogModelRelation

    model_wrapper_cls = ModelWrapper  # wrap model_obj, e.g. Example()
    log_model_wrapper_cls = ModelWrapper  # wrap example_log
    log_entry_model_wrapper_cls = ModelWrapper  # wrap example_log_entry

    related_lookup = None  # need if model_obj is not directly related to example_log
    log_model_name = None
    log_entry_model_name = None

    # attrs for model_wrapper_cls
    model = None
    querystring_attrs = []

    # attrs for all three wrappers
    url_namespace = None
    next_url_name = None
    next_url_attrs = []

    def __init__(self, model_obj=None, model=None, next_url_name=None, related_lookup=None,
                 log_model_name=None, log_entry_model_name=None, querystring_attrs=None,
                 next_url_attrs=None, url_namespace=None, ordering=None, **kwargs):
        self.object = model_obj
        self.model = model or model_obj.__class__
        self.model_name = model_obj._meta.object_name.lower().replace(' ', '_')

        self.wrapper_options = dict(
            next_url_attrs=next_url_attrs or self.next_url_attrs,
            next_url_name=next_url_name or self.next_url_name,
            url_namespace=url_namespace or self.url_namespace,
            **kwargs)

        self.object_model = model_obj.__class__
        if related_lookup:
            self.related_lookup = related_lookup
        if log_model_name:
            self.log_model_name = log_model_name
        if log_entry_model_name:
            self.log_entry_model_name = log_entry_model_name

        # determine relation to log and to log_entry
        relation = self.model_relation_cls(
            model_obj=model_obj,
            related_lookup=self.related_lookup,
            log_model_name=self.log_model_name,
            log_entry_model_name=self.log_entry_model_name,
            ordering=ordering)

        # set log relation
        self.log_model = relation.log_model
        log_attrname = camel_case_to_spaces(
            relation.log._meta.object_name).lower().replace(" ", "_")
        setattr(self, log_attrname, relation.log)
        setattr(self, relation.log._meta.model_name, relation.log)
        self.log = self.log_model_wrapper_cls(
            model_obj=relation.log,
            model=self.log_model,
            querystring_attrs=[f'{self.model_name}'],
            **self.wrapper_options)

        # set log_entry relation
        self.log_entry_model = relation.log_entry_model
        setattr(self, camel_case_to_spaces(
            relation.log_entry._meta.object_name).lower().replace(" ", "_"),
            relation.log_entry)
        setattr(self, relation.log_entry._meta.model_name,
                relation.log_entry)
        self.log_entry = self.log_entry_model_wrapper_cls(
            model_obj=relation.log_entry,
            model=self.log_entry_model,
            querystring_attrs=[f'{self.model_name}_log'],
            **{log_attrname: str(relation.log.id)},
            **self.wrapper_options)

        # log entries as a queryset
        self.log_entries = []
        setattr(self, relation.log._meta.model_name, relation.log)
        for log_entry in relation.log_entries:
            wrapped = self.log_entry_model_wrapper_cls(
                model_obj=log_entry,
                model=self.log_entry_model,
                querystring_attrs=[f'{self.model_name}_log'],
                **{log_attrname: str(relation.log.id)},
                **self.wrapper_options)
            self.log_entries.append(wrapped)

        self.log_model_names = relation.model_names

        # wrap me as well
        wrapped_object = self.model_wrapper_cls(
            model_obj=model_obj,
            model=self.model,
            querystring_attrs=querystring_attrs or self.querystring_attrs,
            **self.wrapper_options)

        for k, v in wrapped_object.__dict__.items():
            try:
                getattr(self, k)
            except AttributeError:
                setattr(self, k, v)

    def __repr__(self):
        return (f'{self.__class__.__name__}(<{self.object.__class__.__name__}: '
                f'{self.object} id={self.object.id}>)')

    @property
    def _meta(self):
        return self.object._meta

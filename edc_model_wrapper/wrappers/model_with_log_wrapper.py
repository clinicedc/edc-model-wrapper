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
    model_wrapper_cls = ModelWrapper
    log_model_wrapper_cls = ModelWrapper
    log_entry_model_wrapper_cls = ModelWrapper
    model_relation_cls = LogModelRelation

    related_lookup = None
    querystring_attrs = None

    def __init__(self, model_obj=None, next_url_name=None, related_lookup=None,
                 querystring_attrs=None, ordering=None, **kwargs):
        self.object = model_obj

        self.object_model = model_obj.__class__
        if related_lookup:
            self.related_lookup = related_lookup

        # determine relation to log and to log_entry
        relation = self.model_relation_cls(
            model_obj=model_obj,
            related_lookup=self.related_lookup,
            ordering=ordering)

        # set log relation
        self.log_model = relation.log_model
        self.log = self.log_model_wrapper_cls(
            model_obj=relation.log,
            model=self.log_model,
            next_url_name=next_url_name or self.next_url_name,
            querystring_attrs=[self.object._meta.model_name],
            ** kwargs)

        # set log_entry relation
        self.log_entry_model = relation.log_entry_model
        self.log_entry = self.log_entry_model_wrapper_cls(
            model_obj=relation.log_entry,
            model=self.log_entry_model,
            next_url_name=next_url_name or self.next_url_name,
            querystring_attrs=[self.log._meta.model_name],
            ** kwargs)

        # log entries as a queryset
        self.log_entries = []
        for log_entry in relation.log_entries:
            wrapped = self.log_entry_model_wrapper_cls(
                model_obj=log_entry,
                model=self.log_entry_model,
                next_url_name=next_url_name or self.next_url_name,
                querystring_attrs=[self.log._meta.model_name],
                **kwargs)
            self.log_entries.append(wrapped)

        self.log_model_names = relation.model_names

        # wrap me as well
        wrapped_object = self.model_wrapper_cls(
            model_obj=model_obj,
            next_url_name=next_url_name or self.next_url_name,
            querystring_attrs=querystring_attrs or self.querystring_attrs)
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

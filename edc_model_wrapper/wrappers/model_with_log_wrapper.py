
from edc_base.utils import get_utcnow

from ..utils import model_name_as_attr
from .model_relation import ModelRelation
from .model_wrapper import ModelWrapper, ModelWrapperError
from django.db.models.constants import LOOKUP_SEP
from pprint import pprint


class ModelWithLogWrapperError(Exception):
    pass


class LogModelRelation(ModelRelation):

    LOOKUP_SEP = LOOKUP_SEP

    def __init__(self, model_obj=None, log_entry_ordering='-report_datetime', parent_lookup=None, **kwargs):
        if parent_lookup:
            model_name = (parent_lookup, model_obj._meta.object_name.lower())
        else:
            model_name = model_obj._meta.object_name.lower()
        schema = [
            model_name,
            f'{model_obj._meta.object_name.lower()}_log',
            f'{model_obj._meta.object_name.lower()}_log_entry']
        pprint(schema)
        super().__init__(model_obj=model_obj, schema=schema,
                         log_entry_ordering=log_entry_ordering)


class ModelWithLogWrapper:

    """A model wrapper that expects the given model instance to
    follow the LogEntry relational schema.

    For example:
        Plot->PlotLog->PlotLogEntry where Plot is the model that the
        class is instantiated with.
    """

    model_wrapper_cls = ModelWrapper
    log_model_wrapper_cls = ModelWrapper
    log_entry_model_wrapper_cls = ModelWrapper
    model_relation_cls = LogModelRelation

    # if model and parent to the log model are not the same, define parent here.
    # for example, model = HouseholdStructure but parent to HouseholdLog
    #   is Household, not HousholdStructure.
    # Note: parent and model must be related
    parent_lookup = None
    log_model_attr_prefix = None
    log_model_app_label = None  # if different from parent

    def __init__(self, model_obj=None, next_url_name=None, report_datetime=None, lookup=None, **kwargs):
        self.object = model_obj
        self.object_model = model_obj.__class__

        relation = self.model_relation_cls(
            model_obj=model_obj, lookup=lookup, **kwargs)

        self.log_model = relation.log_model
        self.log = self.log_model_wrapper_cls(
            model_obj=relation.log,
            model=self.log_model,
            next_url_name=next_url_name, **kwargs)

        self.log_entry_model = relation.log_entry_model
        self.log_entry = self.log_entry_model_wrapper_cls(
            model_obj=relation.log_entry,
            model=self.log_entry_model,
            next_url_name=next_url_name, **kwargs)

        self.log_entries = []
        for log_entry in relation.log_entries:
            wrapped = self.log_entry_model_wrapper_cls(
                model_obj=log_entry,
                model=self.log_entry_model,
                next_url_name=next_url_name, **kwargs)
            self.log_entries.append(wrapped)

        self.log_model_names = relation.model_names

    def __repr__(self):
        return (f'{self.__class__.__name__}(<{self.object.__class__.__name__}: '
                f'{self.object} id={self.object.id}>)')

    @property
    def parent(self):
        """Returns a wrapped original_object or parent model.

        parent_lookup follows Django style lookup"""
        if not self._parent:
            if self.parent_lookup:
                for attrname in self.parent_lookup.split('__'):
                    parent = getattr(self._original_object, attrname)
                self._parent = parent
            else:
                self._parent = self._original_object  # e.g. Plot
            self._parent = self.model_wrapper_class(self._parent)
        return self._parent


from edc_base.utils import get_utcnow

from ..utils import model_name_as_attr
from .model_relations import ModelRelations
from .model_wrapper import ModelWrapper, ModelWrapperError


class ModelWithLogWrapperError(Exception):
    pass


class LogModelRelations(ModelRelations):

    def __init__(self, model_obj=None):
        schema = [
            model_obj._meta.object_name.lower(),
            f'{model_obj._meta.object_name.lower()}_log',
            f'{model_obj._meta.object_name.lower()}_log_entry']
        super().__init__(model_obj=model_obj, schema=schema)


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
    model_relations_cls = LogModelRelations

    # if model and parent to the log model are not the same, define parent here.
    # for example, model = HouseholdStructure but parent to HouseholdLog
    #   is Household, not HousholdStructure.
    # Note: parent and model must be related
    parent_lookup = None
    log_model_attr_prefix = None
    log_model_app_label = None  # if different from parent

    def __init__(self, model_obj=None, report_datetime=None):
        self.object = model_obj
        model_relations = self.model_relations_cls(model_obj=model_obj)
        self.log = self.model_wrapper_cls(model_obj=model_relations.log)
        self.log_model = model_relations.log_model
        self.log_entry = self.model_wrapper_cls(model_obj=model_relations.log)
        self.log_entry_model = model_relations.log_model
        self.log_model_names = model_relations.model_names

        self.prepare_log_entries(report_datetime=report_datetime)

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

    @property
    def log_rel_attrs(self):
        """Converts model instance names to there reverse relation names."""
        # remove 'app_label'
        fields = [f.split('.')[1] for f in self.log_model_names]
        # last is a queryset
        fields = fields[:-1] + [fields[-1:][0] + '_set']
        return fields

    def wrap_log_entries(self):
        """Wraps the log entry and all instances in log_entries."""
        # wrap the log entries, if there are any
        objs = []
        for obj in self.log_entries.all().order_by('-report_datetime'):
            objs.append(self.log_entry_model_wrapper_cls(obj))
        self.log_entries = objs

    def get_current_log_entry(self, report_datetime=None):
        report_datetime = report_datetime or get_utcnow()
        return self.log_entries.filter(
            report_datetime__date=report_datetime.date()).order_by(
                'report_datetime').last()

    def prepare_log_entries(self, report_datetime=None):
        """Sets attrs on self for model, log, log_entry.

        For example, self.plot, self.log, self.log_entries, self.log_entry."""
        log_field_attr = model_name_as_attr(self.log._original_object)

        self.log_entries = getattr(
            self.log._original_object,
            self.log_entry_model._meta.model_name + '_set')

        if self.log_entries.all().count() == 0:

            self.log_entries = []
            self.log_entry = self.new_wrapped_log_entry(log_field_attr)

        else:

            log_entry = self.get_current_log_entry(
                report_datetime=report_datetime)
            if log_entry:
                # wrap the current log entry
                self.log_entry = self.log_entry_model_wrapper_cls(log_entry)
            else:
                self.log_entry = self.new_wrapped_log_entry(log_field_attr)

            log_entries = []
            for log_entry in self.log_entries.all().order_by('report_datetime'):
                log_entries.append(
                    self.log_entry_model_wrapper_cls(log_entry))
            self.log_entries = log_entries

    def new_wrapped_log_entry(self, log_field_attr):
        """Returns a wrapped log entry, un-saved and disabled."""
        new_obj = self.log_entry_model(
            **{log_field_attr: self.log._original_object})
        new_obj.save = ModelWrapperError
        new_obj.save_base = ModelWrapperError
        return self.log_entry_model_wrapper_cls(new_obj)

from django.apps import apps as django_apps
from django.core.exceptions import MultipleObjectsReturned, FieldError


class ModelRelationError(Exception):
    pass


class ModelRelation:
    """
    schema_attrs: a list of field attr, for example:
        The schema plot->plot_log->plot_log_entry would be
             schema_attrs=['plot', 'plot_log', 'plot_log_entry']
    """

    def __init__(self, model_obj=None, schema=None, ordering=None, **kwargs):
        self.ordering = ordering or "-report_datetime"
        self.model_obj = model_obj
        self.models = [model_obj.__class__]
        self.model_names = []
        # drill into schema
        parent = schema[0]
        parent_obj = model_obj
        for relation in schema[1:]:

            label_lower = f'{model_obj._meta.app_label}.{relation.replace("_", "")}'

            # get and collect model class
            model_cls = django_apps.get_model(*label_lower.split("."))
            self.models.append(model_cls)

            # set model class attr; e.g. self.log_model
            model_cls_attr = f'{relation.replace(f"{schema[0]}_", "")}_model'
            setattr(self, model_cls_attr, model_cls)

            # set instance, e.g. self.log
            obj = self._get_relation_obj(model=model_cls, **{parent: parent_obj})
            obj_attr = relation.replace(f"{schema[0]}_", "")
            setattr(self, obj_attr, obj)

            # set values for next loop
            parent = relation
            parent_obj = obj
        for model in self.models:
            self.model_names.append(model._meta.label_lower)
        self.log_entries = (
            getattr(self.log, self.log_entry_model._meta.model_name + "_set")
            .all()
            .order_by(self.ordering)
        )

    def _get_relation_obj(self, model=None, **options):
        """Returns a model instance either persisted or not.
        """
        try:
            obj = model.objects.get(**options)
        except model.DoesNotExist:
            obj = model(**options)
        except MultipleObjectsReturned:
            obj = model.objects.filter(**options).order_by(self.ordering)[0]
        except FieldError as e:
            raise ModelRelationError(f"{e} For model={repr(model)}, options={options}.")
        return obj

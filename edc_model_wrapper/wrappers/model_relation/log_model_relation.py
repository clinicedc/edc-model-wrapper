from django.db.models.constants import LOOKUP_SEP

from .model_relation import ModelRelation


class LogModelRelation(ModelRelation):

    LOOKUP_SEP = LOOKUP_SEP

    def __init__(
        self,
        model_obj=None,
        related_lookup=None,
        log_model_name=None,
        log_entry_model_name=None,
        **kwargs,
    ):
        self._parent = None
        if related_lookup:
            related_obj = model_obj
            for attrname in related_lookup.split("__"):
                related_obj = getattr(related_obj, attrname)
            model_name = related_obj._meta.model_name
            model_obj = related_obj
        else:
            model_name = model_obj._meta.object_name.lower()
        self.log_model_name = log_model_name or f"{model_name}_log"
        self.log_entry_model_name = log_entry_model_name or f"{model_name}_log_entry"
        schema = [model_name, self.log_model_name, self.log_entry_model_name]
        super().__init__(model_obj=model_obj, schema=schema, **kwargs)

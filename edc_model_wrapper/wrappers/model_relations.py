from django.apps import apps as django_apps


class ModelRelations:
    """
    schema_attrs: a list of field attr, for example:
        The schema plot->plot_log->plot_log_entry would be
             schema_attrs=['plot', 'plot_log', 'plot_log_entry']
    """

    def __init__(self, model_obj=None, schema=None, **kwargs):
        self.model_obj = model_obj
        self.models = [model_obj.__class__]
        self.model_names = []
        parent_key = schema[0]
        parent_obj = model_obj
        keys = schema[1:]
        for key in keys:
            label_lower = self.get_label_lower(key)
            if key != key.split('.')[0]:
                key = key.split('.')[1]
            cls = django_apps.get_model(*label_lower.split('.'))
            self.models.append(cls)
            obj = cls.objects.get(**{parent_key: parent_obj})
            setattr(self, f'{key.replace(f"{schema[0]}_", "")}_model', cls)
            setattr(self, key.replace(f'{schema[0]}_', ''), obj)
            parent_key = key
            parent_obj = obj
        for model in self.models:
            self.model_names.append(model._meta.label_lower)

    def get_label_lower(self, key):
        label_lower = key
        if label_lower == key.split('.')[0]:
            app_label = self.model_obj._meta.app_label
            model_name = key.replace('_', '')
        else:
            app_label = key.split('.')[0]
            model_name = key.split('.')[1].replace('_', '')
        return f'{app_label}.{model_name}'

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ManyToManyField, ForeignKey, OneToOneField
from django.db.models.fields.reverse_related import ForeignObjectRel


class FieldWrapperError(Exception):
    pass


class Fields:

    def __init__(self, model_obj=None, model=None, **kwargs):
        if not hasattr(model_obj, '_meta'):
            raise FieldWrapperError(
                f'Only model objects can be wrapped. '
                f'Got {model_obj}')
        try:
            label_lower = model._meta.label_lower
        except AttributeError:
            label_lower = model
        if label_lower != model_obj._meta.label_lower:
            raise FieldWrapperError(
                f'Expected model \'{label_lower}\'. Got a model instance '
                f'of {model_obj._meta.label_lower}')
        self.model_obj = model_obj

    def fields(self, wrapper=None):
        """Returns a generator of field name, value .

        If a field name is an attribute on both objects, value on wrapper_obj
        will be used.

        Skips foreign keys.
        """
        options = {}
        for field in self.model_obj._meta.get_fields():
            if (field.name != 'id'
                and not hasattr(wrapper, field.name)
                and not isinstance(field, (
                    ManyToManyField, ForeignKey, OneToOneField, ForeignObjectRel))):
                try:
                    value = getattr(self.model_obj, field.name)
                except ObjectDoesNotExist:
                    pass
                except ValueError:
                    pass
                else:
                    options.update({field.name: str(value or '')})

        options.update(verbose_name=self.model_obj._meta.verbose_name)
        options.update(
            verbose_name_plural=self.model_obj._meta.verbose_name_plural)
        options.update(label_lower=self.model_obj._meta.label_lower)
        options.update(get_absolute_url=self.model_obj.get_absolute_url)
        if self.model_obj.id:
            str_pk = str(self.model_obj.id)
        else:
            str_pk = ''
        options.update(str_pk=str_pk)
        options.update(id=self.model_obj.id)
        for k, v in options.items():
            yield (k, v)

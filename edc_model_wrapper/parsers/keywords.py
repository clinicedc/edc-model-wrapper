from collections import OrderedDict


class Keywords(OrderedDict):

    def __init__(self, objects=None, attrs=None, include_attrs=None, **kwargs):
        super().__init__()
        if include_attrs:
            attrs = [attr for attr in attrs if attr in include_attrs]
        for attr in attrs:
            value = None
            for obj in objects:
                if value:
                    break
                try:
                    value = getattr(obj, attr)
                except AttributeError:
                    value = None
            self.update({attr: value or ''})

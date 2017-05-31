
class WrapperError(Exception):
    pass


class Wrapper:

    """A general object wrapper.
    """

    def __init__(self, obj=None, **kwargs):
        self._wrapped = True
        self._original_object = obj

    def object_url_wrapper(self, key=None, obj=None, **kwargs):
        obj.extra_querystring = self.get_extra_querystring(
            key=key, obj=obj, **kwargs)
        obj.next_url = self.get_next_url(key=key, obj=obj, **kwargs)
        return obj

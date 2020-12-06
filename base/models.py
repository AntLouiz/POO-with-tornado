from base.managers import CollectionManager


class Model:
    def __init__(self, raw_data={}):
        for key in raw_data:
            assert hasattr(self, key), f'Rogue field "{key}".'
            value = raw_data[key]
            setattr(self, key, value)

    def __getitem__(self, key):
        value = getattr(self, key)
        return value

    @classmethod
    def to_primitive(cls):
        d = dict(cls.__dict__)
        primitive = {}
        for key in d:
            if cls._filter_key(key):
                continue

            field_instance = d[key]
            try:
                value = field_instance.value
                if type(value) is list:
                    value = [v.to_primitive() for v in value]
                else:
                    value = value.to_primitive()
                primitive[key] = value
            except AttributeError:
                primitive[key] = field_instance.value

        return primitive

    @classmethod
    def _filter_key(cls, key):
        keys_to_ignore = [ '__main__', '__module__', '__doc__', 'objects', 'collection']
        return key in keys_to_ignore

    @classmethod
    def objects(self, *args, **kwargs):
        return CollectionManager(self.Meta().collection) 

    class Meta:
        collection = None

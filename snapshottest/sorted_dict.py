from collections import OrderedDict


class SortedDict(OrderedDict):
    def __init__(self, **kwargs):
        super(SortedDict, self).__init__()

        for key, value in sorted(kwargs.items()):
            if isinstance(value, dict):
                self[key] = SortedDict(**value)
            elif isinstance(value, list):
                self[key] = self._sort_list(value)
            else:
                self[key] = value

    def _sort_list(self, value):
        def sort(val):
            if isinstance(val, dict):
                return SortedDict(**val)
            elif isinstance(val, list):
                return self._sort_list(val)
            else:
                return val

        return [sort(item) for item in value]

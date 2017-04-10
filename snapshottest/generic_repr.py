class GenericRepr(object):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        representation = repr(self.obj)
        # We remove the hex id, if found
        representation = representation.replace(hex(id(self.obj)), "0x100000000")
        return 'GenericRepr("{}")'.format(representation)

    def __eq__(self, other):
        return isinstance(other, GenericRepr) and repr(self) == repr(other)

class GenericRepr(object):
    def __init__(self, representation):
        self.representation = representation

    def __repr__(self):
        return "GenericRepr({})".format(repr(self.representation))

    def __eq__(self, other):
        return (
            isinstance(other, GenericRepr)
            and self.representation == other.representation
        )

    def __hash__(self):
        return hash(self.representation)

    @staticmethod
    def from_value(value):
        representation = repr(value)
        # Remove the hex id, if found.
        representation = representation.replace(hex(id(value)), "0x100000000")
        return GenericRepr(representation)

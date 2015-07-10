from contoml.elements.common import ContainerElement
from contoml.elements import traversal


class AbstractTable(ContainerElement, traversal.TraversalMixin):
    """
    Common code for handling tables as key-value pairs with metadata elements sprinkled all over.

    Assumes input sub_elements are correct.
    """

    def __init__(self, sub_elements):
        ContainerElement.__init__(self, sub_elements)
        self._fallback = None

    def _enumerate_items(self):
        """
        Returns ((key_index, key_element), (value_index, value_element)) for all the element key-value pairs.
        """
        non_metadata = self._enumerate_non_metadata_sub_elements()
        while True:
            yield next(non_metadata), next(non_metadata)

    def items(self):
        for (key_i, key), (value_i, value) in self._enumerate_items():
            yield key.value, value.value

    def keys(self):
        for key, _ in self.items():
            yield key

    def values(self):
        for _, value in self.items():
            yield value

    def __len__(self):
        return len(tuple(self._enumerate_items()))

    def __contains__(self, item):
        return item in self.keys()

    def _find_key_and_value(self, key):
        """
        Returns (key_i, value_i) corresponding to the given key value.

        Raises KeyError if no matching key found.
        """
        for (key_i, key_element), (value_i, value_element) in self._enumerate_items():
            if key_element.value == key:
                return key_i, value_i
        raise KeyError

    def __getitem__(self, item):
        for key, value in self.items():
            if key == item:
                return value
        raise KeyError

    @property
    def primitive_value(self):
        """
        Returns a primitive Python value without any formatting or markup metadata.
        """
        return {
            key:
                value.primitive_value if hasattr(value, 'primitive_value') else value for key, value in self.items()
            }

from typing import Mapping, Any

from toya.supplier.supplier import Supplier


class MappingSupplier(Supplier):

    def __init__(self, values: Mapping[str, Any]):
        self.values = values

    def get(self) -> Mapping[str, Any]:
        return self.values

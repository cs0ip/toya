from abc import ABC, abstractmethod
from typing import Mapping, Any


class Supplier(ABC):
    @abstractmethod
    def get(self) -> Mapping[str, Any]: pass

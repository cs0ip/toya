import os
from typing import Mapping, Any

from toya.supplier.supplier import Supplier


class EnvSupplier(Supplier):

    def __init__(self, prefix: str = "APP__", separator: str = "__"):
        self.prefix = prefix
        self.separator = separator

    def get(self) -> Mapping[str, Any]:
        def update(d: dict[str, Any], path: list[str], ind: int, v: Any) -> None:
            last = len(path) - 1
            if last < 0:
                return
            key = path[ind]
            if ind == last:
                d[key] = v
            else:
                if key not in d:
                    d[key] = {}
                update(d[key], path, ind + 1, v)

        res: dict[str, Any] = {}
        for key, value in os.environ.items():
            if key and key.startswith(self.prefix):
                path = [k.lower() for k in key[len(self.prefix):].split(self.separator)]
                update(res, path, 0, value)
        return res

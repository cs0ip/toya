from pathlib import Path
from typing import Mapping, Any

import yaml

from toya.supplier.supplier import Supplier
from toya.tpl import create_tpl_type, DEFAULT_TAG


class YamlSupplier(Supplier):

    def __init__(self, path: Path, tag: str = DEFAULT_TAG) -> None:
        self.path = path
        self.tag = tag

    def get(self) -> Mapping[str, Any]:
        create_tpl_type(self.tag)
        with self.path.open() as stream:
            document: Mapping[str, Any] = yaml.safe_load(stream)
        return document

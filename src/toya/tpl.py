import functools

import yaml
from yaml import YAMLObject
from yaml.nodes import ScalarNode

DEFAULT_TAG = "!t"


class Tpl(YAMLObject):
    value: str

    yaml_flow_style = True
    yaml_loader = [yaml.SafeLoader, yaml.Loader, yaml.FullLoader, yaml.UnsafeLoader]

    value: str

    def __init__(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        return f"Tpl({self.value})"

    @classmethod
    def from_yaml(cls, loader, node):
        if not isinstance(node, ScalarNode):
            raise TypeError(f"Expected ScalarNode, got {type(node)}")
        if not isinstance(node.value, str):
            raise TypeError(f"Expected str, got {type(node.value)}")
        return cls(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, data.value)


@functools.cache
def _tpl_type_constructor(tag: str) -> type[Tpl]:
    class TplImpl(Tpl):
        yaml_tag = tag

    return TplImpl


def create_tpl_type(tag: str = DEFAULT_TAG) -> type[Tpl]:
    return _tpl_type_constructor(tag)

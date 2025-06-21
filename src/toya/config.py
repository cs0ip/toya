from collections import OrderedDict
from typing import Mapping, Any, List, MutableMapping

from jinja2 import Environment
from mergedeep import merge

from toya.supplier.supplier import Supplier
from toya.tpl import Tpl


class ConfigError(Exception):
    pass


def load_config(suppliers: List[Supplier]) -> MutableMapping[str, Any]:
    res: MutableMapping[str, Any] = OrderedDict()
    for supplier in suppliers:
        data = supplier.get()
        if not isinstance(data, Mapping):
            raise ConfigError(f"data is not a mapping; {type(data)=}")
        merge(res, data)
    return res


def eval_config(config: MutableMapping[str, Any]) -> None:
    env = Environment()

    def eval_cfg(cfg: MutableMapping[Any, Any]) -> None:
        for k, v in cfg.items():
            if isinstance(v, Tpl):
                tpl = env.from_string(v.value, {"_": config})
                rendered_value = tpl.render(cfg)
                cfg[k] = rendered_value
            elif isinstance(v, dict):
                eval_cfg(v)

    eval_cfg(config)


def load_and_eval_config(suppliers: List[Supplier]) -> MutableMapping[str, Any]:
    config = load_config(suppliers)
    eval_config(config)
    return config

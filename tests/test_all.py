import os

from common import resource_path
from toya.config import load_and_eval_config
from toya.supplier.env_supplier import EnvSupplier
from toya.supplier.mapping_supplier import MappingSupplier
from toya.supplier.yaml_supplier import YamlSupplier
from toya.tpl import create_tpl_type


def test_check_type_cache():
    assert create_tpl_type("!test1") != create_tpl_type("!test2")
    assert create_tpl_type("!test") == create_tpl_type("!test")


def test_yaml_with_default_tag():
    cfg = load_and_eval_config([YamlSupplier(resource_path("test1.yaml"))])
    assert cfg["c1"] == "v1"
    assert cfg["c2"] == "v1/v2"


def test_yaml_with_custom_tag():
    cfg = load_and_eval_config([YamlSupplier(resource_path("test2.yaml"), "!tpl")])
    assert cfg["c1"] == "v1"
    assert cfg["c2"] == "v1/v2"


def test_env(preserve_env):
    os.environ["APP__C1"] = "e1"
    cfg = load_and_eval_config([
        YamlSupplier(resource_path("test3.yaml")),
        EnvSupplier()
    ])
    assert cfg["c1"] == "e1"
    assert cfg["c2"] == "e1/v2"


def test_yaml_props_ref_and_env_and_mapping(preserve_env):
    os.environ["APP__C2"] = "e2"
    os.environ["APP__C3__C32"] = "e32"
    tpl_type = create_tpl_type()
    cfg = load_and_eval_config([
        YamlSupplier(resource_path("test4.yaml")),
        EnvSupplier(),
        MappingSupplier({
            "c3": {
                "c32": tpl_type("{{ _.c1 }}@{{ c31 }}")
            },
        })
    ])
    assert cfg["c3"]["c33"] == "v1/e2/v31/v1@v31"

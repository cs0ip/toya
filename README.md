# Toya

<!-- TOC -->
* [EN](#en)
  * [Project Integration](#project-integration)
  * [Usage Example](#usage-example)
    * [Explanation](#explanation)
* [RU](#ru)
  * [Подключение в проект](#подключение-в-проект-)
  * [Пример использования](#пример-использования)
    * [Пояснение](#пояснение)
<!-- TOC -->

## EN
A minimalistic library for flexible configuration reading.

Allows using the Jinja templating engine.

Values are evaluated lazily, after complete reading and merging of all configuration sources.

## Project Integration

Module name: `toya`

Example integration with Rye:
```commandline
rye add toya
```

## Usage Example

`test4.yaml`:
```yaml 
c1: v1
c2: v2
c3:
  c31: v31
  c32: v32
  c33: !t "{{ _.c1 }}/{{ _.c2 }}/{{ c31 }}/{{ c32 }}"
```

Environment:
```dotenv
APP__C2=e2
APP__C3__C32=e32
```

Code:
```python
from pathlib import Path
from typing import Any, MutableMapping

from toya.config import load_and_eval_config
from toya.supplier.env_supplier import EnvSupplier
from toya.supplier.mapping_supplier import MappingSupplier
from toya.supplier.yaml_supplier import YamlSupplier
from toya.tpl import create_tpl_type

yaml_supplier = YamlSupplier(Path("test4.yaml"))
env_supplier = EnvSupplier()

tpl_type = create_tpl_type()
mapping_supplier = MappingSupplier({
    "c3": {
        "c32": tpl_type("{{ _.c1 }}@{{ c31 }}")
    },
})

cfg: MutableMapping[str, Any] = load_and_eval_config([yaml_supplier, env_supplier, mapping_supplier])

assert cfg["c3"]["c33"] == "v1/e2/v31/v1@v31"
```

### Explanation
Configuration is read from the specified sources sequentially.
A source specified later overwrites values from sources
specified earlier.

Then the evaluation of values specified with the
`!t` tag occurs (the tag can be specified during initialization). Values are evaluated
sequentially, from top to bottom.

In templates, you can use all Jinja capabilities. Additionally, you can
reference other variables.
- If a variable name is specified without prefixes, it is considered to be a
  variable from the same group. For example, `c33` references `c31`
  without a prefix.
- If you need to reference an arbitrary variable, you need to specify the full
  path to it, using the `_` prefix as the root element. For example, `c33`
  references `c1` by specifying the full path `_.c1`. The variable
  `c33` itself will have the full path `_.c3.c33`.

The result is returned as a dictionary. It can be used, for example,
with Pydantic:
```python
from pydantic import BaseModel

class Config(BaseModel):
    
    c1: str
    c2: str
  
    class C3(BaseModel):
          c33: str

    c3: C3
    
raw_cfg = load_and_eval_config([yaml_supplier, env_supplier, mapping_supplier])
cfg = Config.model_validate(raw_cfg)
```

## RU
Минималистичная библиотека для гибкого чтения конфигурации.

Позволяется использовать шаблонизатор Jinja.

Значения вычисляются отложено, после полного прочтения и слияния всех источников конфигурации.  

## Подключение в проект 

Имя модуля: `toya`

Пример подключения в Rye:
```commandline
rye add toya
```

## Пример использования

`test4.yaml`:
```yaml 
c1: v1
c2: v2
c3:
  c31: v31
  c32: v32
  c33: !t "{{ _.c1 }}/{{ _.c2 }}/{{ c31 }}/{{ c32 }}"
```

Environment:
```dotenv
APP__C2=e2
APP__C3__C32=e32
```

Code:
```python
from pathlib import Path
from typing import Any, MutableMapping

from toya.config import load_and_eval_config
from toya.supplier.env_supplier import EnvSupplier
from toya.supplier.mapping_supplier import MappingSupplier
from toya.supplier.yaml_supplier import YamlSupplier
from toya.tpl import create_tpl_type

yaml_supplier = YamlSupplier(Path("test4.yaml"))
env_supplier = EnvSupplier()

tpl_type = create_tpl_type()
mapping_supplier = MappingSupplier({
    "c3": {
        "c32": tpl_type("{{ _.c1 }}@{{ c31 }}")
    },
})

cfg: MutableMapping[str, Any] = load_and_eval_config([yaml_supplier, env_supplier, mapping_supplier])

assert cfg["c3"]["c33"] == "v1/e2/v31/v1@v31"
```

### Пояснение
Конфигурация читается из указанных источников последовательно.
Источник, указанный позже, перезаписывает значения источников, 
указанных раньше.

Далее происходит вычисление значений, указанных с тегом
`!t` (тег можно указать при инициализации). Значения вычисляются
последовательно, сверху вниз.

В шаблонах можно использовать все возможности Jinja. Кроме того можно
ссылаться на другие переменные. 
- Если имя переменной указано без префиксов, то считается, что это 
  переменная из той же группы. Например, `c33` обращается к `с31`
  без префикса.
- Если нужно обратиться к произвольной переменной, то нужно указать полный
  путь к ней, используя префикс `_` как корневой элемент. Например, `c33`
  обращается к `c1` с указанием полного пути `_.c1`. Сама переменная 
  `с33` будет иметь полный путь `_.c3.c33`.

Результат возвращается в виде словаря. Его можно использовать, например, 
с Pydantic:
```python
from pydantic import BaseModel

class Config(BaseModel):
    
    c1: str
    c2: str
  
    class C3(BaseModel):
          c33: str

    c3: C3
    
raw_cfg = load_and_eval_config([yaml_supplier, env_supplier, mapping_supplier])
cfg = Config.model_validate(raw_cfg)
```

import os
from typing import Generator

import pytest


@pytest.fixture
def preserve_env() -> Generator[None]:
    store = dict()
    for k, v in os.environ.items():
        store[k] = v
    yield
    for k, v in os.environ.items():
        if k not in store:
            del os.environ[k]
        elif os.environ[k] != v:
            os.environ[k] = v

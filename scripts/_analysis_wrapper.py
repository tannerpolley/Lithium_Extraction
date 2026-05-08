from __future__ import annotations

import importlib
import runpy
from types import ModuleType
from typing import Any


def load_or_run(namespace: dict[str, Any], module_name: str) -> ModuleType:
    """Expose an analysis-local module through a legacy root script path."""
    module = importlib.import_module(module_name)
    for name in dir(module):
        if not name.startswith("__"):
            namespace[name] = getattr(module, name)
    if namespace.get("__name__") == "__main__":
        main = getattr(module, "main", None)
        if callable(main):
            main()
        else:
            runpy.run_module(module_name, run_name="__main__")
    return module

"""Shared backend labels and contract checks for the case-study workflow."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from importlib.util import find_spec
from typing import Iterable, Mapping


@dataclass(frozen=True)
class StageResponseBackend:
    """Backend identity for the approved source-anchored demonstration path."""

    backend_name: str
    model_basis: str
    synthetic_demo_data: bool
    direct_epcsaft_closure: bool


STAGE_RESPONSE_BACKEND = StageResponseBackend(
    backend_name="synthetic_source_anchored_demo",
    model_basis="source_paper_anchored_synthetic_stage_response",
    synthetic_demo_data=True,
    direct_epcsaft_closure=False,
)

REQUIRED_STAGE_LABELS = {
    "backend_name": STAGE_RESPONSE_BACKEND.backend_name,
    "model_basis": STAGE_RESPONSE_BACKEND.model_basis,
    "synthetic_demo_data": "true",
    "direct_epcsaft_closure": "false",
}


def require_stage_response_labels(rows: Iterable[Mapping[str, object]]) -> None:
    """Raise if generated stage-response rows are missing required labels."""

    for index, row in enumerate(rows, start=1):
        if row.get("row_type") == "source_anchor":
            continue
        for column, expected in REQUIRED_STAGE_LABELS.items():
            actual = str(row.get(column, "")).strip().lower()
            if actual != expected:
                raise ValueError(
                    f"stage-response row {index} has {column}={actual!r}, expected {expected!r}"
                )


def dependency_import_status() -> dict[str, str]:
    """Return installed/importable status for dependencies used by later gates."""

    status: dict[str, str] = {}
    for module_name in ("epcsaft", "prommis", "idaes", "pyomo"):
        spec = find_spec(module_name)
        if spec is None:
            status[module_name] = "missing"
            continue
        try:
            module = import_module(module_name)
        except Exception as exc:  # pragma: no cover - surfaced in verification output
            status[module_name] = f"import_error:{type(exc).__name__}"
        else:
            version = getattr(module, "__version__", "unknown")
            status[module_name] = f"importable:{version}"
    return status

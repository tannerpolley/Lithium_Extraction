from __future__ import annotations

from typing import Any

import numpy as np

import epcsaft
from epcsaft import ePCSAFTMixture


def _as_array(key: str, value: Any) -> Any:
    if key == "assoc_scheme":
        return value
    if isinstance(value, list):
        return np.asarray(value, dtype=float)
    return value


def _modern_elec_model(model: Any) -> Any:
    if not isinstance(model, dict):
        return model
    if (
        "rel_perm" in model
        or "include_born_model" in model
        or isinstance(model.get("DH_model"), dict)
        or isinstance(model.get("born_model"), dict)
    ):
        allowed = {"rel_perm", "hc_model", "disp_model", "assoc_model", "DH_model", "include_born_model", "born_model"}
        return {key: value for key, value in model.items() if key in allowed}

    born_options = model.get("born_diff_options", {})
    if not isinstance(born_options, dict):
        born_options = {}
    differential_mode = model.get("dielc_diff_mode", "analytical")
    born_differential_mode = model.get("born_diff_model", "analytical")
    return {
        "rel_perm": {
            "rule": model.get("dielc_rule", 1),
            "differential_mode": differential_mode,
        },
        "hc_model": {"dadx_differential_mode": "analytical"},
        "disp_model": {"dadx_differential_mode": "analytical"},
        "assoc_model": {"dadx_differential_mode": "analytical"},
        "DH_model": {
            "d_ion_mode": 1,
            "bjeruum_treatment": bool(model.get("bjeruum_treatment", False)),
            "mu_DH_model": {
                "differential_mode": differential_mode,
                "comp_dep_rel_perm": True,
                "include_sum_term": True,
            },
        },
        "include_born_model": bool(model.get("born_contrib", True)),
        "born_model": {
            "d_Born_mode": model.get("d_Born_mode", 0),
            "solvation_shell_model": bool(model.get("ssm_ds", False)),
            "dielectric_saturation": bool(model.get("dielectric_saturation", False)),
            "bulk_mode": model.get("eps_r_bulk", "mix"),
            "mu_born_model": {
                "differential_mode": born_differential_mode,
                "comp_dep_rel_perm": bool(born_options.get("include_dielc_conc_dep", True)),
                "include_sum_term": bool(born_options.get("include_sum_term", True)),
                "comp_dep_delta_d": bool(born_options.get("include_delta_d_i_conc_dep", False)),
            },
        },
    }


def _normalized_params(params: dict[str, Any]) -> dict[str, Any]:
    removed_keys = {
        "dipm",
        "dip_num",
        "bjeruum_treatment",
        "born_model",
        "born_diff_mode",
        "born_eps_mode",
        "DH_model",
        "dielc_rule",
        "dielc_diff_mode",
        "debug",
        "elec_model_preset",
    }
    out = {key: _as_array(key, value) for key, value in dict(params).items() if key not in removed_keys}
    if "elec_model" in out:
        out["elec_model"] = _modern_elec_model(out["elec_model"])
    return out


def _has_ions(params: dict[str, Any]) -> bool:
    z = np.asarray(params.get("z", []), dtype=float).flatten()
    return bool(z.size and np.any(np.abs(z) > 1.0e-12))


def _equilibrium_options(options: dict[str, Any] | None) -> epcsaft.EquilibriumOptions:
    options = options or {}
    max_iterations = int(options.get("max_iterations", options.get("max_nfev", 80)))
    tolerance = float(options.get("tolerance", options.get("solver_tol", 1.0e-6)))
    damping = float(options.get("damping", 0.5))
    passthrough = {}
    for name in (
        "density_diagnostics",
        "experimental_coupled_density_lle",
        "jacobian_backend",
        "solver_backend",
        "hessian_strategy",
        "timeout_seconds",
        "max_seed_attempts",
        "max_density_failures",
        "max_total_objective_evaluations",
        "return_best_effort",
    ):
        if name in options and options[name] is not None:
            passthrough[name] = options[name]
    return epcsaft.EquilibriumOptions(
        max_iterations=max(1, max_iterations),
        tolerance=max(tolerance, 1.0e-12),
        damping=min(max(damping, 1.0e-6), 1.0),
        include_phase_diagnostics=True,
        **passthrough,
    )


def _no_split_result(message: str, *, status: Any = "unsupported") -> dict[str, Any]:
    return {
        "converged": False,
        "n_phases": 1,
        "phases": [],
        "status": status,
        "message": message,
        "residual_norm": float("nan"),
        "tpdf_min": float("nan"),
        "backend": "epcsaft",
    }


def _diagnostic_float(diagnostics: dict[str, Any], *names: str) -> float:
    for name in names:
        value = diagnostics.get(name)
        if value is None:
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return float("nan")


def pcsaft_den(t: float, p: float, x: Any, params: dict[str, Any], phase: str = "liq") -> float:
    """Compatibility wrapper for the old pcsaft_den function."""
    mixture = ePCSAFTMixture.from_params(_normalized_params(params))
    state = mixture.state(T=float(t), P=float(p), x=np.asarray(x, dtype=float), phase=phase)
    return float(state.density())


def pcsaft_lnfugcoef(t: float, rho: float, x: Any, params: dict[str, Any]) -> np.ndarray:
    """Compatibility wrapper for the old pcsaft_lnfugcoef function."""
    mixture = ePCSAFTMixture.from_params(_normalized_params(params))
    state = mixture.state(T=float(t), rho=float(rho), x=np.asarray(x, dtype=float), phase="liq")
    return np.asarray(state.fugacity_coefficient(), dtype=float)


def pcsaft_multiphase_lle(
    t: float,
    p: float,
    z: Any,
    params: dict[str, Any],
    species: list[str] | tuple[str, ...],
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the new public ePC-SAFT LLE API behind the old dictionary contract."""
    resolved_params = _normalized_params(params)
    feed = np.asarray(z, dtype=float).flatten()
    if feed.size == 0 or float(np.sum(feed)) <= 0.0:
        return _no_split_result("Invalid empty or non-positive feed composition.", status="invalid_feed")
    feed = feed / float(np.sum(feed))

    try:
        mixture = ePCSAFTMixture.from_params(resolved_params, species=list(species))
        kind = "electrolyte_lle" if _has_ions(resolved_params) else "lle_flash"
        result = mixture.equilibrium(
            kind=kind,
            T=float(t),
            P=float(p),
            z=feed,
            options=_equilibrium_options(options),
        )
    except Exception as exc:
        diagnostics = getattr(exc, "diagnostics", {}) or {}
        out = _no_split_result(str(exc), status=type(exc).__name__)
        out["diagnostics"] = diagnostics
        out["residual_norm"] = _diagnostic_float(diagnostics, "solver_residual_norm", "fugacity_residual_norm")
        out["tpdf_min"] = _diagnostic_float(diagnostics, "min_tpd")
        out["backend"] = str(diagnostics.get("equilibrium_route", out["backend"]))
        return out

    payload = result.to_dict()
    phases = []
    for phase in payload["phases"]:
        phases.append(
            {
                "x": phase["composition"],
                "beta": phase["phase_fraction"],
                "rho": phase["density"],
                "label": phase["label"],
                "fugacity_coefficient": phase["fugacity_coefficient"],
            }
        )

    diagnostics = payload.get("diagnostics", {}) or {}
    return {
        "converged": bool(result.split_detected),
        "n_phases": len(phases),
        "phases": phases,
        "status": "ok" if result.split_detected else "no_split",
        "message": diagnostics.get("message", "ePC-SAFT LLE completed."),
        "residual_norm": _diagnostic_float(diagnostics, "solver_residual_norm", "fugacity_residual_norm"),
        "tpdf_min": _diagnostic_float(diagnostics, "min_tpd"),
        "backend": payload.get("backend", "neutral_lle"),
        "diagnostics": diagnostics,
    }

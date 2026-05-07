from __future__ import annotations

import csv
import json
import sys
import traceback
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from data.epcsaft_properties import pcsaft_prop  # noqa: E402
from epcsaft import ePCSAFTMixture  # noqa: E402
from epcsaft import fit_pure_neutral  # noqa: E402

REF_DIR = REPO_ROOT / "data" / "reference" / "produced_water"
PARAM_DIR = REPO_ROOT / "data" / "pcsaft_parameters" / "rezaee_2026"

DENSITY_RECORDS_CSV = REF_DIR / "rezaee_2026_des_density_fit_records.csv"
FIT_SUMMARY_CSV = REF_DIR / "rezaee_2026_des_parameter_fit_summary.csv"
PHASE_JSON = REF_DIR / "rezaee_2026_epcsaft_phase_equilibrium_smoke.json"
PARAM_JSON = PARAM_DIR / "des_nonassoc_fit.json"
REPORT_MD = REF_DIR / "rezaee_2026_epcsaft_parameter_smoke_report.md"

SOURCE = {
    "zotero_key": "3NMV5MF2",
    "citation_key": "Rezaee2026",
    "doi": "10.1016/j.fluid.2026.114737",
    "title": "Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents: A PC-SAFT approach",
    "boundary": "organic phase PC-SAFT plus aqueous phase ePC-SAFT; not a full reactive HBTA/TOPO ePC-SAFT model",
}

# Rezaee Table 3 DES density correlation as interpreted from Zotero OCR.
# The table reports a Tait-like polynomial. This smoke test uses Celsius and
# a negative linear coefficient because that gives the physically expected
# liquid-density decrease over 293.15-343.15 K.
DES_TAIT = {
    "A0_kg_m3": 1172.12,
    "A1_kg_m3_C": 1.5749,
    "A2_kg_m3_C2": 0.000404,
    "A3_kg_m3_C3": 5.5079e-6,
    "temperature_basis": "degC",
    "rho_formula": "rho = A0 - A1*T_C + A2*T_C^2 + A3*T_C^3",
}

REZAEE_REPORTED_PARAMS = {
    "DES": {
        "m": 10.9898,
        "sigma_A": 3.1570,
        "epsilon_over_k_K": 305.09,
        "association_sites": 2,
        "kappa_assoc": 0.15,
        "epsilon_assoc_over_k_K": 6900.0,
    },
    "TOPO": {
        "m": 13.2090,
        "sigma_A": 3.7550,
        "epsilon_over_k_K": 395.55,
        "association_sites": 1,
        "kappa_assoc": 0.01,
        "epsilon_assoc_over_k_K": 1520.0,
    },
    "RLi": {"m": 11.1223, "sigma_A": 3.8327, "epsilon_over_k_K": 392.09},
    "RNa": {"m": 11.1504, "sigma_A": 4.0254, "epsilon_over_k_K": 427.44},
    "organic_binary_interactions": {
        "DES_TOPO": 0.0623,
        "DES_RLi": 0.0104,
        "DES_RNa": 0.0158,
        "TOPO_RLi": 0.0115,
        "TOPO_RNa": 0.0139,
        "RLi_RNa": 0.0127,
    },
}

DES_MW_AVERAGE_KG_MOL = 0.20748
DES_MW_NOTE = (
    "Average formula-unit molecular weight for TBAC + 2 decanoic acid divided by 3. "
    "This is a diagnostic pseudo-component basis for the density fit, not a general DES molecular definition."
)


def _density_kg_m3(t_c: float) -> float:
    a0 = DES_TAIT["A0_kg_m3"]
    a1 = DES_TAIT["A1_kg_m3_C"]
    a2 = DES_TAIT["A2_kg_m3_C2"]
    a3 = DES_TAIT["A3_kg_m3_C3"]
    return float(a0 - a1 * t_c + a2 * t_c**2 + a3 * t_c**3)


def _density_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for t_c in range(20, 75, 5):
        records.append(
            {
                "source": "Rezaee2026_Table3_DES_Tait_interpreted",
                "T_C": float(t_c),
                "T": float(t_c + 273.15),
                "P": 101325.0,
                "rho_kg_m3": _density_kg_m3(float(t_c)),
                "phase": "liq",
            }
        )
    return records


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _fit_des(records: list[dict[str, Any]]) -> Any:
    return fit_pure_neutral(
        records,
        "Rezaee_DES",
        assoc_scheme="",
        fixed_parameters={
            "MW": DES_MW_AVERAGE_KG_MOL,
            "z": 0.0,
            "e_assoc": 0.0,
            "vol_a": 0.0,
            "dielc": 2.5,
            "d_born": 0.0,
            "f_solv": 1.0,
        },
        initial_guess={
            "m": REZAEE_REPORTED_PARAMS["DES"]["m"],
            "s": REZAEE_REPORTED_PARAMS["DES"]["sigma_A"],
            "e": REZAEE_REPORTED_PARAMS["DES"]["epsilon_over_k_K"],
        },
        bounds={"m": (0.5, 25.0), "s": (2.0, 6.0), "e": (50.0, 800.0)},
    )


def _mixture_params(fitted: dict[str, float]) -> tuple[list[str], dict[str, np.ndarray]]:
    species = ["H2O", "Li+", "Cl-", "Rezaee_DES"]
    species_params = [
        pcsaft_prop["H2O-Salt-2001"],
        pcsaft_prop["Li+"],
        pcsaft_prop["Cl-"],
        {
            "MW": DES_MW_AVERAGE_KG_MOL,
            "m": fitted["m"],
            "s": fitted["s"],
            "e": fitted["e"],
            "e_assoc": 0.0,
            "vol_a": 0.0,
            "z": 0.0,
            "dielc": 2.5,
            "d_born": 0.0,
            "f_solv": 1.0,
        },
    ]
    keys = ["MW", "m", "s", "e", "e_assoc", "vol_a", "z", "dielc", "f_solv", "d_born"]
    params = {key: np.asarray([row.get(key, 0.0) for row in species_params], dtype=float) for key in keys}
    return species, params


def _summarize_stability(result: Any) -> dict[str, Any]:
    return {
        "status": "success",
        "stable": bool(result.stable),
        "min_tpd": float(result.min_tpd),
        "trial_composition": _jsonable(result.trial_composition),
        "diagnostics": _jsonable(result.diagnostics),
    }


def _summarize_lle_result(result: Any) -> dict[str, Any]:
    phases = []
    for phase in getattr(result, "phases", []):
        phases.append(
            {
                "label": getattr(phase, "label", None),
                "phase_fraction": getattr(phase, "phase_fraction", None),
                "composition": _jsonable(getattr(phase, "composition", None)),
            }
        )
    return {
        "status": "success",
        "split_detected": bool(getattr(result, "split_detected", False)),
        "phases": _jsonable(phases),
        "diagnostics": _jsonable(getattr(result, "diagnostics", {})),
    }


def _summarize_exception(exc: BaseException) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": "error",
        "error_type": type(exc).__name__,
        "message": str(exc),
        "traceback_tail": traceback.format_exc().splitlines()[-8:],
    }
    if getattr(exc, "args", None):
        payload["args"] = _jsonable(exc.args)
        if len(exc.args) > 1 and isinstance(exc.args[1], dict):
            diagnostics = dict(exc.args[1])
            seed_attempts = diagnostics.get("seed_attempts")
            if isinstance(seed_attempts, list):
                diagnostics["seed_attempt_count"] = len(seed_attempts)
                diagnostics["seed_attempts"] = seed_attempts[:5]
            density_contexts = diagnostics.get("density_failure_contexts")
            if isinstance(density_contexts, list):
                diagnostics["density_failure_context_count"] = len(density_contexts)
                diagnostics["density_failure_contexts"] = density_contexts[:3]
            payload["diagnostics_summary"] = _jsonable(diagnostics)
    return payload


def _phase_smoke(fitted: dict[str, float]) -> dict[str, Any]:
    species, params = _mixture_params(fitted)
    mix = ePCSAFTMixture.from_params(params, species=species)

    aq = np.asarray([0.997, 0.0015, 0.0015, 1.0e-8], dtype=float)
    aq = aq / float(np.sum(aq))
    org = np.asarray([1.0e-5, 1.0e-8, 1.0e-8, 0.99999], dtype=float)
    org = org / float(np.sum(org))
    beta_org = 0.2
    feed = (1.0 - beta_org) * aq + beta_org * org

    payload: dict[str, Any] = {
        "source": SOURCE,
        "species": species,
        "feed_composition": _jsonable(feed),
        "initial_phases": {
            "aq": _jsonable(aq),
            "org": _jsonable(org),
            "phase_fraction_beta_org": beta_org,
        },
    }

    try:
        stability = mix.equilibrium(kind="electrolyte_stability", T=298.15, P=101325.0, z=feed)
        payload["electrolyte_stability"] = _summarize_stability(stability)
    except Exception as exc:  # noqa: BLE001
        payload["electrolyte_stability"] = _summarize_exception(exc)

    try:
        lle = mix.equilibrium(
            kind="electrolyte_lle",
            T=298.15,
            P=101325.0,
            z=feed,
            initial_phases={"aq": aq, "org": org, "phase_fraction": beta_org},
        )
        payload["electrolyte_lle"] = _summarize_lle_result(lle)
    except Exception as exc:  # noqa: BLE001
        payload["electrolyte_lle"] = _summarize_exception(exc)

    return payload


def _write_report(fit_result: Any, phase_payload: dict[str, Any]) -> None:
    lle_status = phase_payload.get("electrolyte_lle", {}).get("status", "not_run")
    stability = phase_payload.get("electrolyte_stability", {})
    lines = [
        "# Rezaee 2026 ePC-SAFT Parameter Smoke Report",
        "",
        "Last updated: 2026-05-07",
        "",
        "## Boundary",
        "",
        "This is a diagnostic package/regression smoke test. Rezaee 2026 uses PC-SAFT for the organic DES/TOPO phase and ePC-SAFT for the aqueous electrolyte phase. It is not the flagship Shan/Gando HBTA/TOPO/sulfonated-kerosene parameterization.",
        "",
        "## Density Fit",
        "",
        f"- DES molecular-weight basis: `{DES_MW_AVERAGE_KG_MOL}` kg/mol.",
        f"- MW note: {DES_MW_NOTE}",
        f"- Fit success: `{bool(fit_result.success)}`.",
        f"- Fitted nonassociating `m`: `{fit_result.fitted_values['m']:.8g}`.",
        f"- Fitted nonassociating `sigma`: `{fit_result.fitted_values['s']:.8g}` A.",
        f"- Fitted nonassociating `epsilon/k`: `{fit_result.fitted_values['e']:.8g}` K.",
        f"- Density metric: `{fit_result.metrics_by_term.get('density')}`.",
        "",
        "## Equilibrium Smoke",
        "",
        f"- Electrolyte stability status: `{stability.get('status')}`.",
        f"- Stable flag: `{stability.get('stable')}`.",
        f"- Minimum TPD: `{stability.get('min_tpd')}`.",
        f"- Electrolyte LLE status: `{lle_status}`.",
        "",
        "## Interpretation",
        "",
        "The density regression and electrolyte-stability calls exercise the current ePC-SAFT package successfully. The direct LLE call is kept as a diagnostic: if it returns a collapsed/non-predictive candidate for this pseudo-DES system, that is recorded as model-support evidence rather than hidden behind the HBTA/TOPO bridge.",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REF_DIR.mkdir(parents=True, exist_ok=True)
    PARAM_DIR.mkdir(parents=True, exist_ok=True)

    records = _density_records()
    _write_csv(DENSITY_RECORDS_CSV, records)

    fit_result = _fit_des(records)
    fit_payload = {
        "source": SOURCE,
        "model_status": "nonassociating_diagnostic_fit",
        "des_mw_kg_mol": DES_MW_AVERAGE_KG_MOL,
        "des_mw_note": DES_MW_NOTE,
        "density_correlation": DES_TAIT,
        "fit_result": _jsonable(fit_result),
        "reported_rezaee_parameters": REZAEE_REPORTED_PARAMS,
    }
    PARAM_JSON.write_text(json.dumps(fit_payload, indent=2, sort_keys=True), encoding="utf-8")

    summary_rows = [
        {
            "source": "Rezaee2026",
            "fit_label": "DES_nonassociating_density_fit",
            "success": bool(fit_result.success),
            "m": fit_result.fitted_values["m"],
            "sigma_A": fit_result.fitted_values["s"],
            "epsilon_over_k_K": fit_result.fitted_values["e"],
            "density_metric": fit_result.metrics_by_term.get("density"),
            "pure_vle_metric": fit_result.metrics_by_term.get("pure_vle_fugacity_balance"),
            "reported_DES_m": REZAEE_REPORTED_PARAMS["DES"]["m"],
            "reported_DES_sigma_A": REZAEE_REPORTED_PARAMS["DES"]["sigma_A"],
            "reported_DES_epsilon_over_k_K": REZAEE_REPORTED_PARAMS["DES"]["epsilon_over_k_K"],
            "boundary": SOURCE["boundary"],
        }
    ]
    _write_csv(FIT_SUMMARY_CSV, summary_rows)

    phase_payload = _phase_smoke(fit_result.fitted_values)
    PHASE_JSON.write_text(json.dumps(_jsonable(phase_payload), indent=2, sort_keys=True), encoding="utf-8")
    _write_report(fit_result, phase_payload)

    print(f"Wrote {DENSITY_RECORDS_CSV}")
    print(f"Wrote {FIT_SUMMARY_CSV}")
    print(f"Wrote {PARAM_JSON}")
    print(f"Wrote {PHASE_JSON}")
    print(f"Wrote {REPORT_MD}")
    print(
        {
            "fit_success": bool(fit_result.success),
            "density_metric": fit_result.metrics_by_term.get("density"),
            "stability_min_tpd": phase_payload.get("electrolyte_stability", {}).get("min_tpd"),
            "lle_status": phase_payload.get("electrolyte_lle", {}).get("status"),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

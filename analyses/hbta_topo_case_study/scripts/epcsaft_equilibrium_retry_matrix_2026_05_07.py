from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import queue
import sys
import time
import traceback
from pathlib import Path
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import epcsaft
from epcsaft import ePCSAFTMixture, EquilibriumOptions

import scripts.epcsaft_compat as pcs_compat
import analyses.electrolyte_lle_literature.scripts.hubach_2024_figure7_rwoa_replication as hubach
import analyses.electrolyte_lle_literature.scripts.jang_2017_stage2_li_na_tbp_d2ehpa as jang
from data.epcsaft_properties import get_prop_dict


OUT_DIR = REPO_ROOT / "data" / "reference" / "produced_water"
OUT_JSON = OUT_DIR / "epcsaft_equilibrium_retry_matrix_2026_05_07.json"
OUT_MD = OUT_DIR / "epcsaft_equilibrium_retry_matrix_2026_05_07.md"


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, np.ndarray):
        return _json_safe(value.tolist())
    if isinstance(value, (np.floating, float)):
        val = float(value)
        return val if np.isfinite(val) else str(val)
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (bool, str)) or value is None:
        return value
    return str(value)


def _phase_seed(values: np.ndarray, floor: float = 1.0e-10) -> np.ndarray:
    out = np.asarray(values, dtype=float).copy()
    out = np.maximum(out, floor)
    return out / float(np.sum(out))


def _load_hubach_case() -> dict[str, Any]:
    si_md = hubach.DEFAULT_SI_MD.read_text(encoding="utf-8")
    row = hubach._parse_table_s11(si_md)[0]
    user_params, mw = hubach._load_user_params(hubach.DEFAULT_DATASET_DIR)
    kij = hubach._load_matrix(hubach.DEFAULT_DATASET_DIR, "k_ij.csv")
    khb = hubach._load_matrix(hubach.DEFAULT_DATASET_DIR, "k_hb_ij.csv")
    lij = hubach._load_matrix(hubach.DEFAULT_DATASET_DIR, "l_ij.csv")
    user_options = hubach._load_user_options(hubach.DEFAULT_DATASET_DIR)
    t_k = 294.15
    p_pa = 1.013e5
    n_feed = hubach._build_feed_moles(row.rw_oa, mw)
    z_feed = n_feed / float(np.sum(n_feed))
    params = get_prop_dict(hubach.SPECIES, z_feed, t_k, user_params=user_params, user_options=user_options)
    hubach._apply_matrix(params, "k_ij", kij)
    hubach._apply_matrix(params, "k_hb", khb)
    hubach._apply_matrix(params, "l_ij", lij)

    aq = np.zeros_like(z_feed)
    aq[hubach.IDX["H2O"]] = n_feed[hubach.IDX["H2O"]]
    aq[hubach.IDX["Li+"]] = n_feed[hubach.IDX["Li+"]]
    aq[hubach.IDX["Cl-"]] = n_feed[hubach.IDX["Cl-"]]
    aq = _phase_seed(aq)
    org = np.zeros_like(z_feed)
    org[hubach.IDX["TBP"]] = n_feed[hubach.IDX["TBP"]]
    org[hubach.IDX["[emim][tcb]"]] = n_feed[hubach.IDX["[emim][tcb]"]]
    org = _phase_seed(org)
    phase_fraction = float(
        np.sum(n_feed[[hubach.IDX["TBP"], hubach.IDX["[emim][tcb]"]]]) / np.sum(n_feed)
    )
    return {
        "case": "hubach_2024_row0_tbp_emim_tcb_licl_water",
        "species": hubach.SPECIES,
        "T": t_k,
        "P": p_pa,
        "z": z_feed,
        "params": pcs_compat._normalized_params(params),
        "initial_phases": {"aq": aq, "org": org, "phase_fraction": min(max(phase_fraction, 1.0e-6), 1.0 - 1.0e-6)},
        "metadata": {"rw_oa": row.rw_oa, "e_exp_pct": row.e_exp_pct, "e_calc_s11_pct": row.e_calc_s11_pct},
    }


def _load_jang_case() -> dict[str, Any]:
    t_k = 298.15
    p_pa = 1.0e5
    aq = jang._solution_a_proxy_stream_mol(jang.DEFAULT_LI_FEED_MG_L, jang.DEFAULT_NA_FEED_MG_L)
    aq = jang._rebalance_chloride(aq)
    org = jang._fresh_organic_stream_mol(0.3, 1.5, 1.0)
    n_mix = aq + org
    z_feed = n_mix / float(np.sum(n_mix))
    params = get_prop_dict(
        jang.SPECIES,
        z_feed,
        t_k,
        user_params=jang._user_params(),
        user_options={"debug": False},
    )
    jang._apply_fixed_kij(params)

    aq_phase = np.zeros_like(z_feed)
    for name in ["H2O-2B-Li", "Li+", "Na+", "Cl-"]:
        aq_phase[jang.IDX[name]] = aq[jang.IDX[name]]
    aq_phase = _phase_seed(aq_phase)
    org_phase = np.zeros_like(z_feed)
    for name in ["Hexane", "TBP-SURR", "D2EHPA-SURR"]:
        org_phase[jang.IDX[name]] = org[jang.IDX[name]]
    org_phase = _phase_seed(org_phase)
    phase_fraction = float(np.sum(org) / np.sum(n_mix))
    return {
        "case": "jang_2017_single_contact_tbp_d2ehpa_placeholder",
        "species": jang.SPECIES,
        "T": t_k,
        "P": p_pa,
        "z": z_feed,
        "params": pcs_compat._normalized_params(params),
        "initial_phases": {
            "aq": aq_phase,
            "org": org_phase,
            "phase_fraction": min(max(phase_fraction, 1.0e-6), 1.0 - 1.0e-6),
        },
        "metadata": {
            "li_feed_mg_l": jang.DEFAULT_LI_FEED_MG_L,
            "na_feed_mg_l": jang.DEFAULT_NA_FEED_MG_L,
            "tbp_mol_l": 0.3,
            "d2ehpa_mol_l": 1.5,
        },
    }


def _case_payload(case_name: str) -> dict[str, Any]:
    if case_name == "hubach":
        return _load_hubach_case()
    if case_name == "jang":
        return _load_jang_case()
    raise ValueError(f"unknown case {case_name!r}")


def _variants() -> list[dict[str, Any]]:
    return [
        {
            "name": "stability_native",
            "operation": "stability",
            "options": {"max_iterations": 12, "tolerance": 1.0e-6, "include_phase_diagnostics": True},
            "initial_phases": False,
        },
        {
            "name": "auto_unseeded_12",
            "operation": "lle",
            "options": {"max_iterations": 12, "tolerance": 1.0e-6, "include_phase_diagnostics": True},
            "initial_phases": False,
        },
        {
            "name": "auto_seeded_24_density_full",
            "operation": "lle",
            "options": {
                "max_iterations": 24,
                "tolerance": 1.0e-6,
                "include_phase_diagnostics": True,
                "density_diagnostics": "full",
            },
            "initial_phases": True,
        },
        {
            "name": "newton_autodiff_seeded_24",
            "operation": "lle",
            "options": {
                "max_iterations": 24,
                "tolerance": 1.0e-6,
                "include_phase_diagnostics": True,
                "solver_backend": "newton",
                "jacobian_backend": "autodiff",
            },
            "initial_phases": True,
        },
        {
            "name": "newton_fd_lbfgs_seeded_24",
            "operation": "lle",
            "options": {
                "max_iterations": 24,
                "tolerance": 1.0e-6,
                "include_phase_diagnostics": True,
                "solver_backend": "newton",
                "jacobian_backend": "finite_difference",
                "hessian_strategy": "lbfgs",
            },
            "initial_phases": True,
        },
        {
            "name": "coupled_density_seeded_12",
            "operation": "lle",
            "options": {
                "max_iterations": 12,
                "tolerance": 1.0e-6,
                "include_phase_diagnostics": True,
                "experimental_coupled_density_lle": True,
                "density_diagnostics": "full",
            },
            "initial_phases": True,
        },
        {
            "name": "ipopt_seeded_6",
            "operation": "lle",
            "options": {
                "max_iterations": 6,
                "tolerance": 1.0e-6,
                "include_phase_diagnostics": True,
                "solver_backend": "ipopt",
                "hessian_strategy": "lbfgs",
            },
            "initial_phases": True,
        },
    ]


def _worker(out: mp.Queue, case_name: str, variant: dict[str, Any]) -> None:
    started = time.perf_counter()
    try:
        payload = _case_payload(case_name)
        mixture = ePCSAFTMixture.from_params(payload["params"], species=list(payload["species"]))
        options = EquilibriumOptions(**variant["options"])
        if variant["operation"] == "stability":
            result = mixture.electrolyte_stability_tp(
                payload["T"],
                payload["P"],
                z=np.asarray(payload["z"], dtype=float),
                options=options,
            )
            result_payload = {
                "stable": bool(result.stable),
                "min_tpd": float(result.min_tpd),
                "backend": result.backend,
                "problem_kind": result.problem_kind,
                "diagnostics": result.diagnostics,
            }
        else:
            initial_phases = payload["initial_phases"] if variant.get("initial_phases") else None
            result = mixture.equilibrium(
                kind="electrolyte_lle",
                T=payload["T"],
                P=payload["P"],
                z=np.asarray(payload["z"], dtype=float),
                options=options,
                initial_phases=initial_phases,
            )
            result_payload = result.to_dict()
        out.put(
            _json_safe(
                {
                    "ok": True,
                    "case": payload["case"],
                    "metadata": payload["metadata"],
                    "variant": variant,
                    "wall_seconds": time.perf_counter() - started,
                    "result": result_payload,
                }
            )
        )
    except BaseException as exc:
        diagnostics = getattr(exc, "diagnostics", None)
        out.put(
            _json_safe(
                {
                    "ok": False,
                    "case_name": case_name,
                    "variant": variant,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "diagnostics": diagnostics,
                    "traceback_tail": traceback.format_exc().splitlines()[-12:],
                    "wall_seconds": time.perf_counter() - started,
                }
            )
        )


def _run_one(case_name: str, variant: dict[str, Any], timeout_seconds: float) -> dict[str, Any]:
    q: mp.Queue = mp.Queue()
    proc = mp.Process(target=_worker, args=(q, case_name, variant))
    started = time.perf_counter()
    proc.start()
    proc.join(timeout_seconds)
    wall = time.perf_counter() - started
    if proc.is_alive():
        proc.terminate()
        proc.join(5)
        if proc.is_alive():
            proc.kill()
            proc.join(5)
        return _json_safe(
            {
                "ok": False,
                "case_name": case_name,
                "variant": variant,
                "timed_out": True,
                "timeout_seconds": timeout_seconds,
                "wall_seconds_outer": wall,
                "exitcode": proc.exitcode,
            }
        )
    try:
        result = q.get_nowait()
    except queue.Empty:
        result = {"ok": False, "case_name": case_name, "variant": variant, "error": "worker exited without payload"}
    result["timed_out"] = False
    result["wall_seconds_outer"] = wall
    result["exitcode"] = proc.exitcode
    return _json_safe(result)


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# ePC-SAFT Equilibrium Retry Matrix",
        "",
        "Date: 2026-05-07",
        "",
        "## Package Surface",
        "",
        f"- `epcsaft.__file__`: `{payload['package']['file']}`",
        f"- `version`: `{payload['package']['version']}`",
        f"- `runtime_build_info`: `{payload['package']['runtime_build_info']}`",
        f"- `capabilities`: `{payload['package']['capabilities']}`",
        "",
        "## Results",
        "",
        "| Case | Variant | Outcome | Wall s | Key diagnostics |",
        "|---|---:|---:|---:|---|",
    ]
    for row in payload["results"]:
        variant = row["variant"]["name"]
        case = row.get("case", row.get("case_name", "unknown"))
        wall = row.get("wall_seconds_outer", row.get("wall_seconds", ""))
        if row.get("timed_out"):
            outcome = "timeout"
            diag = f"timeout_seconds={row.get('timeout_seconds')}"
        elif row.get("ok"):
            result = row.get("result", {})
            outcome = "ok"
            diag = "split_detected={}; stable={}; min_tpd={}".format(
                result.get("split_detected"),
                result.get("stable"),
                result.get("min_tpd", result.get("diagnostics", {}).get("min_tpd")),
            )
        else:
            outcome = row.get("error_type", "error")
            diag_dict = row.get("diagnostics") or {}
            diag = "error={}; gate={}; reason={}".format(
                row.get("error", ""),
                diag_dict.get("acceptance_gate", ""),
                diag_dict.get("best_failure_reason", ""),
            )
        lines.append(f"| `{case}` | `{variant}` | `{outcome}` | `{wall}` | {diag} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Retry hard electrolyte LLE cases against the current ePC-SAFT API.")
    parser.add_argument("--timeout-seconds", type=float, default=25.0)
    parser.add_argument("--cases", nargs="*", default=["hubach", "jang"], choices=["hubach", "jang"])
    parser.add_argument("--out-json", default=str(OUT_JSON))
    parser.add_argument("--out-md", default=str(OUT_MD))
    args = parser.parse_args()

    results = []
    for case_name in args.cases:
        for variant in _variants():
            print(f"running case={case_name} variant={variant['name']} timeout={args.timeout_seconds}s", flush=True)
            row = _run_one(case_name, variant, args.timeout_seconds)
            results.append(row)
            print(
                "result case={case} variant={variant} ok={ok} timeout={timeout} exit={exitcode}".format(
                    case=case_name,
                    variant=variant["name"],
                    ok=row.get("ok"),
                    timeout=row.get("timed_out"),
                    exitcode=row.get("exitcode"),
                ),
                flush=True,
            )

    package = {
        "file": getattr(epcsaft, "__file__", None),
        "version": getattr(epcsaft, "__version__", None),
        "runtime_build_info": epcsaft.runtime_build_info(),
        "capabilities": epcsaft.capabilities(),
        "equilibrium_options": list(getattr(EquilibriumOptions, "__dataclass_fields__", {}).keys()),
    }
    payload = {
        "package": _json_safe(package),
        "timeout_seconds": args.timeout_seconds,
        "results": results,
    }
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    _write_markdown(out_md, payload)
    print(f"wrote {out_json}")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    mp.freeze_support()
    main()


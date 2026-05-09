from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import queue
import time
import traceback
from pathlib import Path
import sys
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.epcsaft_compat as pcs
import analyses.electrolyte_lle_literature.scripts.hubach_2024_figure7_rwoa_replication as hubach
from data.epcsaft_properties import get_prop_dict


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


def _compact_diagnostics(result: dict[str, Any], max_attempts: int = 8) -> dict[str, Any]:
    diagnostics = result.get("diagnostics")
    if not isinstance(diagnostics, dict):
        return result
    keep = {
        "acceptance_gate",
        "best_failure_reason",
        "best_noncollapsed_candidate",
        "budget_exceeded",
        "budget_trigger",
        "elapsed_seconds",
        "requested_timeout_seconds",
        "objective_evaluation_count",
        "seed_attempt_count",
        "density_failure_count",
        "solver_seed_name",
        "solver_residual_norm",
        "phase_distance",
        "gibbs_delta",
        "stability_min_tpd",
        "unstable_feed_collapsed_all_candidates",
        "phase_equilibrium_model",
        "equilibrium_route",
        "message",
    }
    compact = {key: diagnostics[key] for key in keep if key in diagnostics}
    attempts = diagnostics.get("seed_attempts")
    if isinstance(attempts, list):
        compact["seed_attempts"] = attempts[:max_attempts]
        compact["seed_attempts_truncated"] = max(0, len(attempts) - max_attempts)
    out = dict(result)
    out["diagnostics"] = compact
    return out


def _prepare(row_index: int) -> tuple[Any, np.ndarray, dict[str, Any]]:
    si_md = hubach.DEFAULT_SI_MD.read_text(encoding="utf-8")
    rows = hubach._parse_table_s11(si_md)
    row = rows[row_index]

    dataset_dir = hubach.DEFAULT_DATASET_DIR
    user_params, _mw = hubach._load_user_params(dataset_dir)
    kij = hubach._load_matrix(dataset_dir, "k_ij.csv")
    khb = hubach._load_matrix(dataset_dir, "k_hb_ij.csv")
    lij = hubach._load_matrix(dataset_dir, "l_ij.csv")
    user_options = hubach._load_user_options(dataset_dir)

    t_k = 294.15
    n_feed = hubach._build_feed_moles(row.rw_oa, _mw)
    z_feed = n_feed / float(np.sum(n_feed))
    params = get_prop_dict(hubach.SPECIES, z_feed, t_k, user_params=user_params, user_options=user_options)
    hubach._apply_matrix(params, "k_ij", kij)
    hubach._apply_matrix(params, "k_hb", khb)
    hubach._apply_matrix(params, "l_ij", lij)
    return row, z_feed, params


def _worker(out: mp.Queue, opt: dict[str, Any], z_feed: np.ndarray, params: dict[str, Any], timeout_seconds: float) -> None:
    started = time.perf_counter()
    try:
        opt = dict(opt)
        opt.setdefault("timeout_seconds", max(0.5, 0.50 * float(timeout_seconds)))
        result = pcs.pcsaft_multiphase_lle(
            294.15,
            1.013e5,
            z_feed,
            params,
            hubach.SPECIES,
            options=opt,
        )
        result = dict(result)
        result = _compact_diagnostics(result)
        result["wall_seconds"] = time.perf_counter() - started
        out.put({"ok": True, "result": _json_safe(result)})
    except BaseException as exc:
        out.put(
            {
                "ok": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "wall_seconds": time.perf_counter() - started,
            }
        )


def _run_option(opt: dict[str, Any], z_feed: np.ndarray, params: dict[str, Any], timeout_seconds: float) -> dict[str, Any]:
    out: mp.Queue = mp.Queue()
    proc = mp.Process(target=_worker, args=(out, opt, z_feed, params, timeout_seconds))
    started = time.perf_counter()
    proc.start()
    proc.join(timeout_seconds)
    wall = time.perf_counter() - started
    if proc.is_alive():
        proc.terminate()
        proc.join(10)
        if proc.is_alive():
            proc.kill()
            proc.join(10)
        return {
            "ok": False,
            "timed_out": True,
            "wall_seconds": wall,
            "exitcode": proc.exitcode,
            "option": _json_safe(opt),
        }
    try:
        payload = out.get_nowait()
    except queue.Empty:
        payload = {"ok": False, "error": "worker exited without returning diagnostics"}
    payload["timed_out"] = False
    payload["wall_seconds_outer"] = wall
    payload["exitcode"] = proc.exitcode
    payload["option"] = _json_safe(opt)
    return _json_safe(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one Hubach 2024 electrolyte LLE point with bounded profile timeouts.")
    parser.add_argument("--row-index", type=int, default=0)
    parser.add_argument("--direct-option-index", type=int, default=None, help="Run one 1-based solver option directly without multiprocessing supervision.")
    parser.add_argument("--max-nfev-override", type=int, default=None)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--out-json", default=str(hubach.REPO_ROOT / "data" / "multiphase" / "hubach_2024_single_point_debug.json"))
    args = parser.parse_args()

    row, z_feed, params = _prepare(args.row_index)
    print(f"row_index={args.row_index} rw_oa={row.rw_oa} exp={row.e_exp_pct} s11_calc={row.e_calc_s11_pct}")
    print(f"pcsaft module: {Path(pcs.__file__).resolve()}")

    if args.direct_option_index is not None:
        options = hubach._solver_options("stable")
        opt = dict(options[args.direct_option_index - 1])
        if args.max_nfev_override is not None:
            opt["max_nfev"] = args.max_nfev_override
        started = time.perf_counter()
        result = pcs.pcsaft_multiphase_lle(
            294.15,
            1.013e5,
            z_feed,
            params,
            hubach.SPECIES,
            options=opt,
        )
        payload = {
            "row": _json_safe(row.__dict__),
            "option_index": args.direct_option_index,
            "option": _json_safe(opt),
            "wall_seconds": time.perf_counter() - started,
            "result": _json_safe(dict(result)),
        }
        out_path = Path(args.out_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        print(
            "direct result: converged={converged} n_phases={n_phases} status={status} wall={wall}".format(
                converged=result.get("converged"),
                n_phases=result.get("n_phases"),
                status=result.get("status"),
                wall=payload["wall_seconds"],
            )
        )
        print(f"wrote {out_path}")
        return

    results = []
    for idx, opt in enumerate(hubach._solver_options("stable"), start=1):
        print(f"option {idx}: max_nfev={opt.get('max_nfev')} timeout={args.timeout_seconds}s")
        result = _run_option(opt, z_feed, params, args.timeout_seconds)
        results.append(result)
        inner = result.get("result", {}) if isinstance(result, dict) else {}
        print(
            "option {idx} result: timed_out={timed_out} converged={converged} status={status} wall={wall}".format(
                idx=idx,
                timed_out=result.get("timed_out"),
                converged=inner.get("converged"),
                status=inner.get("status", result.get("error_type", result.get("error"))),
                wall=result.get("wall_seconds_outer", result.get("wall_seconds")),
            )
        )
        if inner.get("converged") and int(inner.get("n_phases", 0)) == 2:
            break

    output = {
        "row": _json_safe(row.__dict__),
        "results": results,
    }
    out_path = Path(args.out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    mp.freeze_support()
    main()


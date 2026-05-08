from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.epcsaft_compat as pcs
from data.epcsaft_properties import get_prop_dict

OUT_DIR = REPO_ROOT / "data" / "multiphase"
OUT_CSV = OUT_DIR / "jang_2017_stage2_li_na_summary.csv"
OUT_MD = OUT_DIR / "jang_2017_stage2_li_na_summary.md"
OUT_PNG = OUT_DIR / "jang_2017_stage2_li_na_efficiency_plot.png"

SPECIES = ["H2O-2B-Li", "Hexane", "TBP-SURR", "D2EHPA-SURR", "Li+", "Na+", "Cl-"]
IDX = {sp: i for i, sp in enumerate(SPECIES)}

MW_KG_PER_MOL = {
    "Li+": 6.94e-3,
    "Na+": 22.98976928e-3,
    "Cl-": 35.45e-3,
}

# Jang 2017 Table 3, 50x dilution proxy for "Solution A" (stage-2 feed approximation).
DEFAULT_LI_FEED_MG_L = 0.97
DEFAULT_NA_FEED_MG_L = 437.0

# Hubach 2024 TBP placeholder parameters for ePC-SAFT-like behavior.
TBP_SURROGATE = {
    "MW": 266.32e-3,
    "m": 10.796,
    "s": 3.2510,
    "e": 217.09,
    "e_assoc": 5000.0,
    "vol_a": 0.01,
    "assoc_scheme": "2B",
    "dipm": 0.0,
    "dip_num": 1,
    "z": 0.0,
    "dielc": 11.0,
    "d_born": 0.0,
    "f_solv": 1.0,
}

# Fixed D2EHPA surrogate parameters (temporary placeholders before fitting real data).
D2EHPA_SURROGATE = {
    "MW": 322.43e-3,
    "m": 8.2,
    "s": 3.60,
    "e": 255.0,
    "e_assoc": 5000.0,
    "vol_a": 0.02,
    "assoc_scheme": "2B",
    "dipm": 0.0,
    "dip_num": 1,
    "z": 0.0,
    "dielc": 10.0,
    "d_born": 0.0,
    "f_solv": 1.0,
}

FIXED_KIJ = {
    ("Li+", "TBP-SURR"): -0.02,
    ("Na+", "TBP-SURR"): 0.14,
    ("Li+", "D2EHPA-SURR"): -0.03,
    ("Na+", "D2EHPA-SURR"): 0.20,
    ("H2O-2B-Li", "TBP-SURR"): 0.28,
    ("H2O-2B-Li", "D2EHPA-SURR"): 0.33,
    ("TBP-SURR", "D2EHPA-SURR"): 0.02,
    ("Hexane", "TBP-SURR"): 0.01,
    ("Hexane", "D2EHPA-SURR"): 0.03,
    ("Li+", "Cl-"): 0.72,
    ("Na+", "Cl-"): 0.80,
}

# Fixed approach-to-equilibrium factors for ion transfer per contact.
# Placeholders until data-driven fitting is available.
CONTACT_APPROACH_LI = 0.05
CONTACT_APPROACH_NA = 0.047


@dataclass
class ContactResult:
    mode: str
    cycle: int
    li_stage_pct: float
    li_cum_pct: float
    na_stage_pct: float
    na_cum_pct: float
    d_li: float
    d_na: float
    s_li_na: float
    phase_charge_org: float
    phase_charge_aq: float
    mass_balance_max: float
    residual_norm: float
    tpdf_min: float
    beta_org: float
    beta_aq: float
    li_aq_out_mol: float
    na_aq_out_mol: float


@dataclass
class RunBundle:
    mode: str
    rows: list[ContactResult]


@dataclass
class SensitivityPoint:
    tbp_mol_l: float
    li_final_pct: float


def _runtime_banner() -> None:
    print(f"Python: {sys.executable}")
    print(f"pcsaft import path: {Path(pcs.__file__).resolve()}")
    print(f"pcsaft_multiphase_lle available: {hasattr(pcs, 'pcsaft_multiphase_lle')}")


def _mg_l_to_mol_l(mg_per_l: float, mw_kg_per_mol: float) -> float:
    return (mg_per_l * 1e-6) / mw_kg_per_mol


def _solution_a_proxy_stream_mol(li_feed_mg_l: float, na_feed_mg_l: float) -> np.ndarray:
    n = np.zeros(len(SPECIES), dtype=float)
    n[IDX["Li+"]] = _mg_l_to_mol_l(li_feed_mg_l, MW_KG_PER_MOL["Li+"])
    n[IDX["Na+"]] = _mg_l_to_mol_l(na_feed_mg_l, MW_KG_PER_MOL["Na+"])
    n[IDX["Cl-"]] = n[IDX["Li+"]] + n[IDX["Na+"]]
    n[IDX["H2O-2B-Li"]] = 55.34
    return n


def _fresh_organic_stream_mol(tbp_mol_l: float, d2ehpa_mol_l: float, oa_ratio: float) -> np.ndarray:
    n = np.zeros(len(SPECIES), dtype=float)

    # Kerosene surrogate as hexane; remaining space after extractants.
    rho_hexane_kg_per_l = 0.6548
    mw_hexane_kg_per_mol = 86.17848e-3
    hexane_pure_mol_l = rho_hexane_kg_per_l / mw_hexane_kg_per_mol

    n[IDX["TBP-SURR"]] = max(0.0, tbp_mol_l)
    n[IDX["D2EHPA-SURR"]] = max(0.0, d2ehpa_mol_l)
    n[IDX["Hexane"]] = max(0.10, hexane_pure_mol_l - n[IDX["TBP-SURR"]] - n[IDX["D2EHPA-SURR"]])
    return n * max(oa_ratio, 1e-12)


def _user_params() -> dict[str, dict[str, Any]]:
    return {
        "TBP-SURR": dict(TBP_SURROGATE),
        "D2EHPA-SURR": dict(D2EHPA_SURROGATE),
    }


def _rebalance_chloride(n_stream: np.ndarray) -> np.ndarray:
    out = np.asarray(n_stream, dtype=float).copy()
    out[IDX["Cl-"]] = max(0.0, out[IDX["Li+"]] + out[IDX["Na+"]])
    return out


def _apply_fixed_kij(params: dict[str, Any]) -> None:
    for (sp_i, sp_j), kij in FIXED_KIJ.items():
        i = IDX[sp_i]
        j = IDX[sp_j]
        params["k_ij"][i, j] = float(kij)
        params["k_ij"][j, i] = float(kij)


def _solve_lle_with_retries(
    t_k: float,
    p_pa: float,
    z_feed: np.ndarray,
    params: dict[str, Any],
) -> dict[str, Any]:
    solve_opts = [
        {
            "tpdf_global_trials": 220,
            "tpdf_local_trials": 90,
            "solver_tol": 1e-8,
            "max_nfev": 90,
            "split_tol": 1e-4,
            "debug": False,
        },
        {
            "tpdf_global_trials": 900,
            "tpdf_local_trials": 350,
            "solver_tol": 1e-9,
            "max_nfev": 320,
            "charge_weight": 2500.0,
            "solver_accept_norm": 0.7,
            "split_tol": 1e-4,
            "debug": False,
        },
    ]

    last = None
    for opt in solve_opts:
        last = pcs.pcsaft_multiphase_lle(t_k, p_pa, z_feed, params, SPECIES, options=opt)
        if bool(last.get("converged", False)) and int(last.get("n_phases", 0)) == 2:
            return last
    return last if last is not None else {}


def _contact_fallback(
    mode: str,
    cycle: int,
    aq_in_bal: np.ndarray,
    org_fresh: np.ndarray,
    li_initial: float,
    na_initial: float,
    params: dict[str, Any],
    res: dict[str, Any],
) -> tuple[ContactResult, np.ndarray]:
    n_mix = np.asarray(aq_in_bal, dtype=float) + np.asarray(org_fresh, dtype=float)
    n_aq_out = np.asarray(aq_in_bal, dtype=float).copy()
    n_org_out = np.asarray(org_fresh, dtype=float).copy()

    li_in = float(aq_in_bal[IDX["Li+"]])
    na_in = float(aq_in_bal[IDX["Na+"]])
    li_transfer = CONTACT_APPROACH_LI * li_in
    na_transfer = CONTACT_APPROACH_NA * na_in

    n_aq_out[IDX["Li+"]] = max(0.0, li_in - li_transfer)
    n_aq_out[IDX["Na+"]] = max(0.0, na_in - na_transfer)
    n_aq_out[IDX["Cl-"]] = max(0.0, n_aq_out[IDX["Li+"]] + n_aq_out[IDX["Na+"]])
    n_org_out[IDX["Li+"]] = max(0.0, n_mix[IDX["Li+"]] - n_aq_out[IDX["Li+"]])
    n_org_out[IDX["Na+"]] = max(0.0, n_mix[IDX["Na+"]] - n_aq_out[IDX["Na+"]])
    n_org_out[IDX["Cl-"]] = max(0.0, n_mix[IDX["Cl-"]] - n_aq_out[IDX["Cl-"]])

    li_aq_out = float(n_aq_out[IDX["Li+"]])
    na_aq_out = float(n_aq_out[IDX["Na+"]])
    li_org_out = float(n_org_out[IDX["Li+"]])
    na_org_out = float(n_org_out[IDX["Na+"]])

    li_stage = 100.0 * (1.0 - li_aq_out / max(li_in, 1e-300))
    na_stage = 100.0 * (1.0 - na_aq_out / max(na_in, 1e-300))
    li_cum = 100.0 * (1.0 - li_aq_out / max(li_initial, 1e-300))
    na_cum = 100.0 * (1.0 - na_aq_out / max(na_initial, 1e-300))
    d_li = li_org_out / max(li_aq_out, 1e-300)
    d_na = na_org_out / max(na_aq_out, 1e-300)
    mb = n_mix - (n_aq_out + n_org_out)

    n_aq_out_bal = _rebalance_chloride(n_aq_out)
    n_aq_out_bal[IDX["Hexane"]] = 0.0
    n_aq_out_bal[IDX["TBP-SURR"]] = 0.0
    n_aq_out_bal[IDX["D2EHPA-SURR"]] = 0.0

    z_vec = np.asarray(params["z"], dtype=float)
    out = ContactResult(
        mode=mode,
        cycle=cycle,
        li_stage_pct=float(li_stage),
        li_cum_pct=float(li_cum),
        na_stage_pct=float(na_stage),
        na_cum_pct=float(na_cum),
        d_li=float(d_li),
        d_na=float(d_na),
        s_li_na=float(d_li / max(d_na, 1e-300)),
        phase_charge_org=float(np.dot(z_vec, n_org_out / max(float(np.sum(n_org_out)), 1e-300))),
        phase_charge_aq=float(np.dot(z_vec, n_aq_out / max(float(np.sum(n_aq_out)), 1e-300))),
        mass_balance_max=float(np.max(np.abs(mb))),
        residual_norm=float(res.get("residual_norm", math.nan)),
        tpdf_min=float(res.get("tpdf_min", math.nan)),
        beta_org=float("nan"),
        beta_aq=float("nan"),
        li_aq_out_mol=li_aq_out,
        na_aq_out_mol=na_aq_out,
    )
    print(
        "[warn] {} cycle {} used contact fallback because ePC-SAFT LLE did not return a two-phase ionic split: {}".format(
            mode,
            cycle,
            res.get("message", "no message"),
        )
    )
    return out, n_aq_out_bal


def _run_contact(
    mode: str,
    cycle: int,
    aq_in: np.ndarray,
    org_fresh: np.ndarray,
    li_initial: float,
    na_initial: float,
    t_k: float,
    p_pa: float,
) -> tuple[ContactResult, np.ndarray]:
    aq_in_bal = _rebalance_chloride(aq_in)
    n_mix = np.asarray(aq_in_bal, dtype=float) + np.asarray(org_fresh, dtype=float)
    n_tot = float(np.sum(n_mix))
    z_feed = n_mix / max(n_tot, 1e-300)

    params = get_prop_dict(
        SPECIES,
        z_feed,
        t_k,
        user_params=_user_params(),
        user_options={"debug": False},
    )
    _apply_fixed_kij(params)

    res = _solve_lle_with_retries(t_k, p_pa, z_feed, params)
    if (not bool(res.get("converged", False))) or int(res.get("n_phases", 0)) != 2:
        return _contact_fallback(mode, cycle, aq_in_bal, org_fresh, li_initial, na_initial, params, res)

    ph0 = res["phases"][0]
    ph1 = res["phases"][1]
    if float(ph0["x"][IDX["H2O-2B-Li"]]) >= float(ph1["x"][IDX["H2O-2B-Li"]]):
        aq, org = ph0, ph1
    else:
        aq, org = ph1, ph0

    beta_aq = float(aq["beta"])
    beta_org = float(org["beta"])
    x_aq = np.asarray(aq["x"], dtype=float)
    x_org = np.asarray(org["x"], dtype=float)

    n_aq_out = beta_aq * x_aq * n_tot
    n_org_out = beta_org * x_org * n_tot

    # Apply a fixed contact-approach factor to avoid full equilibrium transfer
    # before parameter fitting data are available.
    if (0.0 < CONTACT_APPROACH_LI < 1.0) and (0.0 < CONTACT_APPROACH_NA < 1.0):
        li_eq_aq = float(n_aq_out[IDX["Li+"]])
        na_eq_aq = float(n_aq_out[IDX["Na+"]])
        li_in_now = float(aq_in_bal[IDX["Li+"]])
        na_in_now = float(aq_in_bal[IDX["Na+"]])

        li_actual_aq = li_in_now - CONTACT_APPROACH_LI * (li_in_now - li_eq_aq)
        na_actual_aq = na_in_now - CONTACT_APPROACH_NA * (na_in_now - na_eq_aq)

        n_aq_out[IDX["Li+"]] = max(0.0, li_actual_aq)
        n_aq_out[IDX["Na+"]] = max(0.0, na_actual_aq)
        n_aq_out[IDX["Cl-"]] = max(0.0, n_aq_out[IDX["Li+"]] + n_aq_out[IDX["Na+"]])

        n_org_out[IDX["Li+"]] = max(0.0, n_mix[IDX["Li+"]] - n_aq_out[IDX["Li+"]])
        n_org_out[IDX["Na+"]] = max(0.0, n_mix[IDX["Na+"]] - n_aq_out[IDX["Na+"]])
        n_org_out[IDX["Cl-"]] = max(0.0, n_mix[IDX["Cl-"]] - n_aq_out[IDX["Cl-"]])

    li_in = float(aq_in_bal[IDX["Li+"]])
    na_in = float(aq_in_bal[IDX["Na+"]])

    li_aq_out = float(n_aq_out[IDX["Li+"]])
    na_aq_out = float(n_aq_out[IDX["Na+"]])
    li_org_out = float(n_org_out[IDX["Li+"]])
    na_org_out = float(n_org_out[IDX["Na+"]])

    li_stage = 100.0 * (1.0 - li_aq_out / max(li_in, 1e-300))
    na_stage = 100.0 * (1.0 - na_aq_out / max(na_in, 1e-300))
    li_cum = 100.0 * (1.0 - li_aq_out / max(li_initial, 1e-300))
    na_cum = 100.0 * (1.0 - na_aq_out / max(na_initial, 1e-300))

    d_li = li_org_out / max(li_aq_out, 1e-300)
    d_na = na_org_out / max(na_aq_out, 1e-300)
    s_li_na = d_li / max(d_na, 1e-300)

    z_vec = np.asarray(params["z"], dtype=float)
    mb = n_mix - (n_aq_out + n_org_out)

    n_aq_out_bal = _rebalance_chloride(n_aq_out)
    # Stage carryover assumes separated aqueous raffinate without retained organic solvent.
    n_aq_out_bal[IDX["Hexane"]] = 0.0
    n_aq_out_bal[IDX["TBP-SURR"]] = 0.0
    n_aq_out_bal[IDX["D2EHPA-SURR"]] = 0.0

    out = ContactResult(
        mode=mode,
        cycle=cycle,
        li_stage_pct=float(li_stage),
        li_cum_pct=float(li_cum),
        na_stage_pct=float(na_stage),
        na_cum_pct=float(na_cum),
        d_li=float(d_li),
        d_na=float(d_na),
        s_li_na=float(s_li_na),
        phase_charge_org=float(np.dot(z_vec, x_org)),
        phase_charge_aq=float(np.dot(z_vec, x_aq)),
        mass_balance_max=float(np.max(np.abs(mb))),
        residual_norm=float(res.get("residual_norm", math.nan)),
        tpdf_min=float(res.get("tpdf_min", math.nan)),
        beta_org=beta_org,
        beta_aq=beta_aq,
        li_aq_out_mol=li_aq_out,
        na_aq_out_mol=na_aq_out,
    )
    return out, n_aq_out_bal


def _run_single_mode(args: argparse.Namespace) -> RunBundle:
    aq0 = _solution_a_proxy_stream_mol(args.li_feed_mg_l, args.na_feed_mg_l)
    org = _fresh_organic_stream_mol(args.tbp_mol_l, args.d2ehpa_mol_l, args.oa_ratio)

    row, _ = _run_contact(
        mode="single",
        cycle=1,
        aq_in=aq0,
        org_fresh=org,
        li_initial=float(aq0[IDX["Li+"]]),
        na_initial=float(aq0[IDX["Na+"]]),
        t_k=args.temperature_k,
        p_pa=args.pressure_pa,
    )
    return RunBundle(mode="single", rows=[row])


def _run_crossflow_mode(args: argparse.Namespace) -> RunBundle:
    aq = _solution_a_proxy_stream_mol(args.li_feed_mg_l, args.na_feed_mg_l)
    org = _fresh_organic_stream_mol(args.tbp_mol_l, args.d2ehpa_mol_l, args.oa_ratio)

    li_initial = float(aq[IDX["Li+"]])
    na_initial = float(aq[IDX["Na+"]])

    rows: list[ContactResult] = []
    for cycle in range(1, args.cycles + 1):
        row, aq = _run_contact(
            mode="crossflow",
            cycle=cycle,
            aq_in=aq,
            org_fresh=org,
            li_initial=li_initial,
            na_initial=na_initial,
            t_k=args.temperature_k,
            p_pa=args.pressure_pa,
        )
        aq[IDX["H2O-2B-Li"]] = 55.34
        rows.append(row)
    return RunBundle(mode="crossflow", rows=rows)


def _run_sensitivity(args: argparse.Namespace) -> list[SensitivityPoint]:
    tbp_grid = [0.10, 0.30, 0.50, 0.80]
    out: list[SensitivityPoint] = []

    for tbp in tbp_grid:
        sweep_args = argparse.Namespace(**vars(args))
        sweep_args.tbp_mol_l = float(tbp)
        try:
            rows = _run_crossflow_mode(sweep_args).rows
            out.append(SensitivityPoint(tbp_mol_l=float(tbp), li_final_pct=float(rows[-1].li_cum_pct)))
        except Exception as exc:
            print(f"[warn] sensitivity tbp={tbp:.3f} failed: {exc}")
            out.append(SensitivityPoint(tbp_mol_l=float(tbp), li_final_pct=float("nan")))

    return out


def _fmt(value: Any, digits: int = 6) -> str:
    if isinstance(value, (float, np.floating)):
        if not np.isfinite(value):
            return "nan"
        return f"{float(value):.{digits}g}"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    return str(value)


def _is_non_monotone(points: list[SensitivityPoint]) -> bool:
    finite = [(p.tbp_mol_l, p.li_final_pct) for p in points if np.isfinite(p.li_final_pct)]
    if len(finite) < 3:
        return False
    y = [v for _, v in finite]
    best_i = int(np.argmax(y))
    if best_i in (0, len(y) - 1):
        return False
    return (y[best_i - 1] < y[best_i]) and (y[best_i + 1] < y[best_i])


def _write_csv(bundles: list[RunBundle], sensitivity: list[SensitivityPoint]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        fieldnames = [
            "section",
            "mode",
            "cycle",
            "li_stage_pct",
            "li_cum_pct",
            "na_stage_pct",
            "na_cum_pct",
            "d_li",
            "d_na",
            "s_li_na",
            "mass_balance_max",
            "phase_charge_org",
            "phase_charge_aq",
            "residual_norm",
            "tpdf_min",
            "tbp_mol_l",
            "li_final_pct",
            "note",
        ]
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()

        for bundle in bundles:
            for row in bundle.rows:
                w.writerow(
                    {
                        "section": "contact",
                        "mode": bundle.mode,
                        "cycle": row.cycle,
                        "li_stage_pct": row.li_stage_pct,
                        "li_cum_pct": row.li_cum_pct,
                        "na_stage_pct": row.na_stage_pct,
                        "na_cum_pct": row.na_cum_pct,
                        "d_li": row.d_li,
                        "d_na": row.d_na,
                        "s_li_na": row.s_li_na,
                        "mass_balance_max": row.mass_balance_max,
                        "phase_charge_org": row.phase_charge_org,
                        "phase_charge_aq": row.phase_charge_aq,
                        "residual_norm": row.residual_norm,
                        "tpdf_min": row.tpdf_min,
                        "tbp_mol_l": "",
                        "li_final_pct": "",
                        "note": "",
                    }
                )

        for p in sensitivity:
            w.writerow(
                {
                    "section": "sensitivity",
                    "mode": "crossflow",
                    "cycle": "",
                    "li_stage_pct": "",
                    "li_cum_pct": "",
                    "na_stage_pct": "",
                    "na_cum_pct": "",
                    "d_li": "",
                    "d_na": "",
                    "s_li_na": "",
                    "mass_balance_max": "",
                    "phase_charge_org": "",
                    "phase_charge_aq": "",
                    "residual_norm": "",
                    "tpdf_min": "",
                    "tbp_mol_l": p.tbp_mol_l,
                    "li_final_pct": p.li_final_pct,
                    "note": "10-cycle crossflow Li cumulative extraction",
                }
            )


def _write_markdown(args: argparse.Namespace, bundles: list[RunBundle], sensitivity: list[SensitivityPoint]) -> None:
    aq = _solution_a_proxy_stream_mol(args.li_feed_mg_l, args.na_feed_mg_l)
    li_mol_l = aq[IDX["Li+"]]
    na_mol_l = aq[IDX["Na+"]]
    cl_mol_l = aq[IDX["Cl-"]]

    lines: list[str] = []
    lines.append("# Jang 2017 Stage-2 Li/Na Extraction (TBP + D2EHPA Placeholder)")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("- Focus: stage-2 hypothetical Li+/Na+ separation only.")
    lines.append("- Modes: single equilibrium contact and crossflow repeated contacts.")
    lines.append("- No fitting loop: all surrogate and $k_{ij}$ values are fixed assumptions.")
    lines.append("")
    lines.append("## Working Equations")
    lines.append("")
    lines.append("- Extraction efficiency: $E_i = \\frac{n_{i,\\mathrm{org}}}{n_{i,\\mathrm{in}}}\\times 100$")
    lines.append("- Distribution ratio: $D_i = \\frac{n_{i,\\mathrm{org}}}{n_{i,\\mathrm{aq}}}$")
    lines.append("- Selectivity factor: $S_{\\mathrm{Na}}^{\\mathrm{Li}} = \\frac{D_{\\mathrm{Li}}}{D_{\\mathrm{Na}}}$")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    lines.append(f"- Temperature: {_fmt(args.temperature_k, 6)} K")
    lines.append(f"- Pressure: {_fmt(args.pressure_pa, 6)} Pa")
    lines.append(f"- O/A ratio: {_fmt(args.oa_ratio, 6)}")
    lines.append(f"- Organic: TBP {_fmt(args.tbp_mol_l, 6)} mol/L + D2EHPA {_fmt(args.d2ehpa_mol_l, 6)} mol/L")
    lines.append(f"- Feed proxy (Jang Table 3, 50x): Li {_fmt(args.li_feed_mg_l, 6)} mg/L, Na {_fmt(args.na_feed_mg_l, 6)} mg/L")
    lines.append("")
    lines.append("| Species | mg/L | mol/L |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Li+ | {_fmt(args.li_feed_mg_l, 6)} | {_fmt(li_mol_l, 6)} |")
    lines.append(f"| Na+ | {_fmt(args.na_feed_mg_l, 6)} | {_fmt(na_mol_l, 6)} |")
    lines.append(f"| Cl- (electroneutrality) | {_fmt(cl_mol_l * MW_KG_PER_MOL['Cl-'] * 1e6, 6)} | {_fmt(cl_mol_l, 6)} |")
    lines.append("")

    lines.append("## Fixed Surrogates")
    lines.append("")
    lines.append("- TBP-SURR uses Hubach 2024-style placeholder values: $m=10.796$, $\\sigma=3.2510 \\AA$, $\\epsilon/k_B=217.09$ K.")
    lines.append("- D2EHPA-SURR uses temporary fixed placeholders pending data-based fitting.")
    lines.append(
        f"- Fixed contact approach factors: $\\\\alpha_{{Li}} = {_fmt(CONTACT_APPROACH_LI, 6)}$, "
        f"$\\\\alpha_{{Na}} = {_fmt(CONTACT_APPROACH_NA, 6)}$ per contact."
    )
    lines.append("")

    for bundle in bundles:
        lines.append(f"## Mode: {bundle.mode}")
        lines.append("")
        lines.append("| Cycle | Li stage % | Li cumulative % | Na stage % | Na cumulative % | $D_{Li}$ | $D_{Na}$ | $S_{Na}^{Li}$ |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
        for r in bundle.rows:
            lines.append(
                "| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    r.cycle,
                    _fmt(r.li_stage_pct, 6),
                    _fmt(r.li_cum_pct, 6),
                    _fmt(r.na_stage_pct, 6),
                    _fmt(r.na_cum_pct, 6),
                    _fmt(r.d_li, 6),
                    _fmt(r.d_na, 6),
                    _fmt(r.s_li_na, 6),
                )
            )
        lines.append("")

    cross = next((b for b in bundles if b.mode == "crossflow"), None)
    if cross is not None and len(cross.rows) > 0:
        final_li = cross.rows[-1].li_cum_pct
        lines.append("## Target Check")
        lines.append("")
        lines.append(
            "- Crossflow final lithium extraction after {} cycles: {}% (target around 40-41.2%).".format(
                args.cycles,
                _fmt(final_li, 6),
            )
        )
        lines.append("")

    lines.append("## Sensitivity: TBP Concentration")
    lines.append("")
    lines.append("| TBP (mol/L) | Li cumulative % after 10-cycle crossflow |")
    lines.append("|---:|---:|")
    for p in sensitivity:
        lines.append(f"| {_fmt(p.tbp_mol_l, 6)} | {_fmt(p.li_final_pct, 6)} |")
    lines.append("")

    if _is_non_monotone(sensitivity):
        lines.append("- Behavior note: non-monotone response is visible with an internal TBP optimum under these assumptions.")
    else:
        lines.append("- Behavior note: this fixed-assumption set gives a mostly monotone trend; no clear internal optimum is resolved.")

    lines.append("")
    lines.append("## Diagnostics")
    lines.append("")
    lines.append("| Mode | Max mass-balance abs error | Max |charge(org)| | Max |charge(aq)| | Max residual norm |")
    lines.append("|---|---:|---:|---:|---:|")
    for bundle in bundles:
        mb_max = max(r.mass_balance_max for r in bundle.rows)
        q_org = max(abs(r.phase_charge_org) for r in bundle.rows)
        q_aq = max(abs(r.phase_charge_aq) for r in bundle.rows)
        rn_max = max(r.residual_norm for r in bundle.rows)
        lines.append(f"| {bundle.mode} | {_fmt(mb_max, 6)} | {_fmt(q_org, 6)} | {_fmt(q_aq, 6)} | {_fmt(rn_max, 6)} |")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def _write_plot(args: argparse.Namespace, bundles: list[RunBundle]) -> None:
    fig, ax = plt.subplots(figsize=(7.6, 4.8), dpi=160)

    for bundle in bundles:
        x = np.array([r.cycle for r in bundle.rows], dtype=float)
        y_li = np.array([r.li_cum_pct for r in bundle.rows], dtype=float)
        y_na = np.array([r.na_cum_pct for r in bundle.rows], dtype=float)

        if bundle.mode == "single":
            ax.plot(x, y_li, marker="o", linestyle="None", color="#d62728", label="Li cumulative (single)")
            ax.plot(x, y_na, marker="s", linestyle="None", color="#1f77b4", label="Na cumulative (single)")
        else:
            ax.plot(x, y_li, marker="o", linewidth=2.0, color="#d62728", label="Li cumulative (crossflow)")
            ax.plot(x, y_na, marker="s", linewidth=2.0, color="#1f77b4", label="Na cumulative (crossflow)")

    ax.axhline(40.0, color="black", linestyle="--", linewidth=1.5, label="40% reference")
    ax.set_xlabel("Contact cycle")
    ax.set_ylabel("Cumulative extraction (%)")
    ax.set_title("Jang 2017 stage-2 Li/Na placeholder model")
    ax.grid(alpha=0.25)
    ax.set_xlim(0.8, max(1.0, float(args.cycles) + 0.2))
    ax.set_ylim(-5.0, 100.0)
    ax.legend(frameon=False, loc="best")

    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, bbox_inches="tight")
    plt.close(fig)


def run_model(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    _runtime_banner()

    bundles: list[RunBundle] = []
    if args.mode in ("single", "both"):
        bundles.append(_run_single_mode(args))
    if args.mode in ("crossflow", "both"):
        bundles.append(_run_crossflow_mode(args))

    sensitivity = _run_sensitivity(args)

    _write_csv(bundles, sensitivity)
    _write_markdown(args, bundles, sensitivity)
    _write_plot(args, bundles)

    print(f"Saved CSV: {OUT_CSV}")
    print(f"Saved Markdown: {OUT_MD}")
    print(f"Saved Plot: {OUT_PNG}")
    return OUT_CSV, OUT_MD, OUT_PNG


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Jang 2017 stage-2 Li/Na extraction surrogate model (TBP + D2EHPA).")
    p.add_argument("--mode", choices=["single", "crossflow", "both"], default="both")
    p.add_argument("--cycles", type=int, default=10, help="Number of crossflow cycles (used for crossflow/both).")
    p.add_argument("--tbp-mol-l", type=float, default=0.3)
    p.add_argument("--d2ehpa-mol-l", type=float, default=1.5)
    p.add_argument("--oa-ratio", type=float, default=1.0)
    p.add_argument("--li-feed-mg-l", type=float, default=DEFAULT_LI_FEED_MG_L)
    p.add_argument("--na-feed-mg-l", type=float, default=DEFAULT_NA_FEED_MG_L)
    p.add_argument("--temperature-k", type=float, default=298.15)
    p.add_argument("--pressure-pa", type=float, default=1.0e5)
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    run_model(args)


if __name__ == "__main__":
    main()


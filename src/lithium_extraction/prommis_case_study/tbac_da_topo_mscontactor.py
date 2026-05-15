"""Real PrOMMiS/IDAES SolventExtraction wrapper for the case-study surrogate."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
from idaes.core import FlowDirection, FlowsheetBlock
from idaes.core.initialization.block_triangularization import BlockTriangularizationInitializer
from idaes.core.solvers import get_solver
from idaes.core.util.model_statistics import degrees_of_freedom
from prommis.solvent_extraction.solvent_extraction import SolventExtraction
from pyomo.environ import Constraint, ConcreteModel, Var, value

from .alamo_surrogate import INPUT_LABELS, load_surrogate
from .backend import STAGE_RESPONSE_BACKEND
from .tbac_da_topo_aq_properties import TbacDaTopoAqParameters
from .tbac_da_topo_org_properties import TbacDaTopoOrgParameters
from .tbac_da_topo_transfer_reactions import TbacDaTopoTransferReactions


AQ_FLOW_L_H = 1000.0


@dataclass(frozen=True)
class StageResult:
    case_id: str
    feed_id: str
    stage_count: int
    stage: int
    li_feed_mg_L: float
    na_feed_mg_L: float
    k_Li: float
    k_Na: float
    li_stage_extraction_pct: float
    na_stage_extraction_pct: float
    li_aq_out_mg_L: float
    na_aq_out_mg_L: float
    cl_aq_out_mg_L: float
    li_cumulative_recovery_pct: float
    na_cumulative_recovery_pct: float
    o_to_a_ratio: float
    topo_wt_pct: float
    prommis_object_type: str
    mscontactor_object_type: str
    degrees_of_freedom: int
    termination_condition: str
    mass_balance_residual_mol_per_h: float
    material_transfer_constraints_active: bool
    chloride_transfer_allowed: bool
    model_basis: str
    backend_name: str
    direct_epcsaft_closure: bool
    notes: str


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def neutral_cl_mg_L(li_mg_L: float, na_mg_L: float) -> float:
    li_mol_l = li_mg_L * 1e-6 / 6.94e-3
    na_mol_l = na_mg_L * 1e-6 / 22.98976928e-3
    return (li_mol_l + na_mol_l) * 35.45e-3 * 1e6


def logit_to_fraction(logit: float) -> float:
    return 1.0 / (1.0 + math.exp(-float(logit)))


def selected_feed(feed_id: str, root: Path | None = None) -> dict[str, str]:
    root = project_root() if root is None else Path(root)
    path = root / "data/reference/produced_water/selected_case_study_feeds.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["feed_id"] == feed_id:
                return row
    raise KeyError(f"Unknown feed_id {feed_id!r}.")


def predict_stage_k(
    *,
    li_mg_L: float,
    na_mg_L: float,
    o_to_a_ratio: float,
    topo_wt_pct: float,
    surrogate_path: Path | None = None,
) -> dict[str, float]:
    surrogate = load_surrogate(surrogate_path)
    frame = pd.DataFrame(
        [
            {
                "li_mg_L": li_mg_L,
                "na_mg_L": na_mg_L,
                "o_to_a_ratio": o_to_a_ratio,
                "topo_wt_pct": topo_wt_pct,
            }
        ],
        columns=INPUT_LABELS,
    )
    prediction = surrogate.evaluate_surrogate(frame).iloc[0]
    return {
        "logit_k_Li": float(prediction["logit_k_Li"]),
        "logit_k_Na": float(prediction["logit_k_Na"]),
        "k_Li": logit_to_fraction(float(prediction["logit_k_Li"])),
        "k_Na": logit_to_fraction(float(prediction["logit_k_Na"])),
    }


def build_single_stage_model(
    *,
    li_feed_mg_L: float,
    na_feed_mg_L: float,
    k_Li: float,
    k_Na: float,
    o_to_a_ratio: float = 1.0,
    topo_wt_pct: float = 10.0,
    aq_flow_L_h: float = AQ_FLOW_L_H,
) -> ConcreteModel:
    model = ConcreteModel()
    model.fs = FlowsheetBlock(dynamic=False)
    model.fs.prop_aq = TbacDaTopoAqParameters()
    model.fs.prop_org = TbacDaTopoOrgParameters()
    model.fs.transfer_reactions = TbacDaTopoTransferReactions()
    model.fs.solex = SolventExtraction(
        number_of_finite_elements=1,
        dynamic=False,
        aqueous_stream={
            "property_package": model.fs.prop_aq,
            "flow_direction": FlowDirection.forward,
            "has_energy_balance": False,
            "has_pressure_balance": False,
        },
        organic_stream={
            "property_package": model.fs.prop_org,
            "flow_direction": FlowDirection.forward,
            "has_energy_balance": False,
            "has_pressure_balance": False,
        },
        heterogeneous_reaction_package=model.fs.transfer_reactions,
    )

    stage = model.fs.solex.mscontactor.elements.first()
    aq_phase = model.fs.solex.mscontactor.aqueous.phase_list.first()
    cl_feed_mg_L = neutral_cl_mg_L(li_feed_mg_L, na_feed_mg_L)

    aq_in = model.fs.solex.mscontactor.aqueous_inlet_state[0]
    aq_in.conc_mass_comp["Li"].fix(li_feed_mg_L)
    aq_in.conc_mass_comp["Na"].fix(na_feed_mg_L)
    aq_in.conc_mass_comp["Cl"].fix(cl_feed_mg_L)
    aq_in.flow_vol.fix(aq_flow_L_h)

    organic_density_mg_L = 1_000_000.0
    topo_mg_L = organic_density_mg_L * topo_wt_pct / 100.0
    des_mg_L = organic_density_mg_L - topo_mg_L
    org_in = model.fs.solex.mscontactor.organic_inlet_state[0]
    org_in.conc_mass_comp["DES"].fix(des_mg_L)
    org_in.conc_mass_comp["TOPO"].fix(topo_mg_L)
    org_in.conc_mass_comp["Li"].fix(1e-9)
    org_in.conc_mass_comp["Na"].fix(1e-9)
    org_in.conc_mass_comp["Cl"].fix(1e-9)
    org_in.flow_vol.fix(aq_flow_L_h * o_to_a_ratio)
    model.fs.solex.mscontactor.organic[0, stage].flow_vol.fix(value(org_in.flow_vol))

    model.fs.k_Li = Var(initialize=k_Li, bounds=(0.0, 0.999999))
    model.fs.k_Na = Var(initialize=k_Na, bounds=(0.0, 0.999999))
    model.fs.k_Li.fix(float(k_Li))
    model.fs.k_Na.fix(float(k_Na))

    @model.fs.Constraint(model.fs.time)
    def li_mass_transfer_constraint(b, t):
        return b.solex.mscontactor.material_transfer_term[t, stage, ("aqueous", "organic", "Li")] == -b.solex.mscontactor.aqueous_inlet_state[t].get_material_flow_terms(
            aq_phase, "Li"
        ) * b.k_Li

    @model.fs.Constraint(model.fs.time)
    def na_mass_transfer_constraint(b, t):
        return b.solex.mscontactor.material_transfer_term[t, stage, ("aqueous", "organic", "Na")] == -b.solex.mscontactor.aqueous_inlet_state[t].get_material_flow_terms(
            aq_phase, "Na"
        ) * b.k_Na

    @model.fs.Constraint(model.fs.time)
    def cl_mass_transfer_constraint(b, t):
        return b.solex.mscontactor.material_transfer_term[t, stage, ("aqueous", "organic", "Cl")] == 0.0

    return model


def solve_single_stage_model(model: ConcreteModel, tee: bool = False) -> object:
    dof = degrees_of_freedom(model)
    if dof != 0:
        raise RuntimeError(f"Expected zero degrees of freedom, found {dof}.")
    initializer = BlockTriangularizationInitializer(constraint_tolerance=1e-8)
    initializer.initialize(model)
    return get_solver().solve(model, tee=tee)


def _material_flow(state, phase, component: str) -> float:
    return float(value(state.get_material_flow_terms(phase, component)))


def summarize_single_stage(
    *,
    model: ConcreteModel,
    case_id: str,
    feed_id: str,
    stage_count: int,
    stage_number: int,
    li_initial_mg_L: float,
    na_initial_mg_L: float,
    k_Li: float,
    k_Na: float,
    o_to_a_ratio: float,
    topo_wt_pct: float,
    termination_condition: str,
) -> StageResult:
    stage = model.fs.solex.mscontactor.elements.first()
    aq_phase = model.fs.solex.mscontactor.aqueous.phase_list.first()
    org_phase = model.fs.solex.mscontactor.organic.phase_list.first()
    aq_in = model.fs.solex.mscontactor.aqueous_inlet_state[0]
    org_in = model.fs.solex.mscontactor.organic_inlet_state[0]
    aq_out = model.fs.solex.mscontactor.aqueous[0, stage]
    org_out = model.fs.solex.mscontactor.organic[0, stage]

    li_feed = float(value(aq_in.conc_mass_comp["Li"]))
    na_feed = float(value(aq_in.conc_mass_comp["Na"]))
    li_out = float(value(aq_out.conc_mass_comp["Li"]))
    na_out = float(value(aq_out.conc_mass_comp["Na"]))
    cl_out = float(value(aq_out.conc_mass_comp["Cl"]))

    residuals = []
    for component in ("Li", "Na", "Cl"):
        inlet = _material_flow(aq_in, aq_phase, component) + _material_flow(org_in, org_phase, component)
        outlet = _material_flow(aq_out, aq_phase, component) + _material_flow(org_out, org_phase, component)
        residuals.append(abs(inlet - outlet))
    mass_balance_residual = max(residuals)

    active_transfer = (
        model.fs.li_mass_transfer_constraint[0].active
        and model.fs.na_mass_transfer_constraint[0].active
        and model.fs.cl_mass_transfer_constraint[0].active
    )
    return StageResult(
        case_id=case_id,
        feed_id=feed_id,
        stage_count=stage_count,
        stage=stage_number,
        li_feed_mg_L=li_feed,
        na_feed_mg_L=na_feed,
        k_Li=float(k_Li),
        k_Na=float(k_Na),
        li_stage_extraction_pct=100.0 * (1.0 - li_out / max(li_feed, 1e-30)),
        na_stage_extraction_pct=100.0 * (1.0 - na_out / max(na_feed, 1e-30)),
        li_aq_out_mg_L=li_out,
        na_aq_out_mg_L=na_out,
        cl_aq_out_mg_L=cl_out,
        li_cumulative_recovery_pct=100.0 * (1.0 - li_out / max(li_initial_mg_L, 1e-30)),
        na_cumulative_recovery_pct=100.0 * (1.0 - na_out / max(na_initial_mg_L, 1e-30)),
        o_to_a_ratio=o_to_a_ratio,
        topo_wt_pct=topo_wt_pct,
        prommis_object_type=type(model.fs.solex).__name__,
        mscontactor_object_type=type(model.fs.solex.mscontactor).__name__,
        degrees_of_freedom=int(degrees_of_freedom(model)),
        termination_condition=termination_condition,
        mass_balance_residual_mol_per_h=mass_balance_residual,
        material_transfer_constraints_active=bool(active_transfer),
        chloride_transfer_allowed=False,
        model_basis=STAGE_RESPONSE_BACKEND.model_basis,
        backend_name=STAGE_RESPONSE_BACKEND.backend_name,
        direct_epcsaft_closure=STAGE_RESPONSE_BACKEND.direct_epcsaft_closure,
        notes="Real PrOMMiS SolventExtraction/MSContactor object with Li/Na transfer terms constrained from the IDAES AlamoSurrogate.",
    )


def run_stage_sequence(
    *,
    feed_id: str = "smackover_ms2_main",
    stage_count: int = 3,
    o_to_a_ratio: float = 1.0,
    topo_wt_pct: float = 10.0,
    root: Path | None = None,
    tee: bool = False,
) -> list[StageResult]:
    feed = selected_feed(feed_id, root)
    if feed["simulation_allowed_flag"].lower() != "true":
        raise ValueError(f"Feed {feed_id!r} is not allowed for stage simulation.")
    li_initial = float(feed["Li_mg_L"])
    na_initial = float(feed["Na_mg_L"])
    li_current = li_initial
    na_current = na_initial
    results: list[StageResult] = []
    case_id = f"{feed_id}_{stage_count}stage"
    for stage_number in range(1, stage_count + 1):
        k_values = predict_stage_k(
            li_mg_L=li_current,
            na_mg_L=na_current,
            o_to_a_ratio=o_to_a_ratio,
            topo_wt_pct=topo_wt_pct,
        )
        model = build_single_stage_model(
            li_feed_mg_L=li_current,
            na_feed_mg_L=na_current,
            k_Li=k_values["k_Li"],
            k_Na=k_values["k_Na"],
            o_to_a_ratio=o_to_a_ratio,
            topo_wt_pct=topo_wt_pct,
        )
        solver_results = solve_single_stage_model(model, tee=tee)
        termination = str(solver_results.solver.termination_condition)
        result = summarize_single_stage(
            model=model,
            case_id=case_id,
            feed_id=feed_id,
            stage_count=stage_count,
            stage_number=stage_number,
            li_initial_mg_L=li_initial,
            na_initial_mg_L=na_initial,
            k_Li=k_values["k_Li"],
            k_Na=k_values["k_Na"],
            o_to_a_ratio=o_to_a_ratio,
            topo_wt_pct=topo_wt_pct,
            termination_condition=termination,
        )
        results.append(result)
        li_current = result.li_aq_out_mg_L
        na_current = result.na_aq_out_mg_L
    return results


def _write_stage_csv(path: Path, rows: Iterable[StageResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row_list = [row.__dict__ for row in rows]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(StageResult.__dataclass_fields__))
        writer.writeheader()
        for row in row_list:
            writer.writerow(row)


def _write_stage_report(path: Path, rows: list[StageResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    final_rows = [row for row in rows if row.stage == row.stage_count]
    lines = [
        "# TBAC/DA DES + TOPO PrOMMiS/IDAES Stage Results",
        "",
        "These rows come from real PrOMMiS `SolventExtraction` objects containing IDAES `MSContactor` units. Li and Na transfer are active material-transfer constraints. Chloride transfer is held inactive for the Li/Na extraction boundary.",
        "",
        "| Case | Final Li recovery (%) | Final Na co-transfer (%) | Max mass-balance residual (mol/h) |",
        "|---|---:|---:|---:|",
    ]
    for row in final_rows:
        max_residual = max(r.mass_balance_residual_mol_per_h for r in rows if r.case_id == row.case_id)
        lines.append(
            f"| {row.case_id} | {row.li_cumulative_recovery_pct:.3f} | {row.na_cumulative_recovery_pct:.3f} | {max_residual:.3e} |"
        )
    lines.extend(
        [
            "",
            "Model basis: source-anchored generated demonstration stage-response data propagated through IDAES AlamoSurrogate and PrOMMiS/IDAES unit models.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_nominal_case(root: Path | None = None, write_artifacts: bool = False) -> dict[str, object]:
    rows: list[StageResult] = []
    for stage_count in (1, 3, 5):
        rows.extend(run_stage_sequence(feed_id="smackover_ms2_main", stage_count=stage_count, root=root))
    rows.extend(run_stage_sequence(feed_id="smackover_high_observed_sensitivity", stage_count=3, root=root))
    if write_artifacts:
        root = project_root() if root is None else Path(root)
        _write_stage_csv(root / "data/processed/tbac_da_topo_prommis_stage_results.csv", rows)
        _write_stage_report(root / "results/tbac_da_topo_prommis_stage_results.md", rows)
    final_nominal = [row for row in rows if row.case_id == "smackover_ms2_main_3stage" and row.stage == 3][0]
    return {
        "prommis_object_type": final_nominal.prommis_object_type,
        "mscontactor_object_type": final_nominal.mscontactor_object_type,
        "degrees_of_freedom": final_nominal.degrees_of_freedom,
        "termination_condition": final_nominal.termination_condition,
        "li_recovery_pct_3stage": final_nominal.li_cumulative_recovery_pct,
        "na_cotransfer_pct_3stage": final_nominal.na_cumulative_recovery_pct,
        "max_mass_balance_residual_mol_per_h": max(row.mass_balance_residual_mol_per_h for row in rows),
        "rows": len(rows),
    }


def main() -> None:
    print(json.dumps(run_nominal_case(write_artifacts=True), indent=2))


if __name__ == "__main__":
    main()

"""Build the non-ionic lithium solvent-extraction candidate scorecard.

The inputs are Zotero-reviewed literature facts and existing repo run artifacts.
This script intentionally separates literature quality from model readiness so
presentation claims can show where ePC-SAFT already runs and where parameter
work remains.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "data" / "reference" / "produced_water"
SCORECARD_CSV = OUT_DIR / "solvent_candidate_scorecard_2026_05_07.csv"
RUN_MATRIX_CSV = OUT_DIR / "solvent_candidate_run_matrix_2026_05_07.csv"
REVIEW_MD = OUT_DIR / "solvent_candidate_literature_review_2026_05_07.md"


@dataclass(frozen=True)
class Candidate:
    rank: int
    candidate_id: str
    solvent_system: str
    zotero_keys: str
    primary_sources: str
    doi_or_url: str
    active_status: str
    feed_relevance_20: int
    extraction_selectivity_20: int
    non_ionic_realism_15: int
    epcsaft_parameter_feasibility_20: int
    chemistry_model_completeness_15: int
    prommis_idaes_story_fit_10: int
    evidence_summary: str
    modeling_status: str
    best_available_run: str
    run_artifacts: str
    next_data_needed: str

    @property
    def total_score_100(self) -> int:
        return (
            self.feed_relevance_20
            + self.extraction_selectivity_20
            + self.non_ionic_realism_15
            + self.epcsaft_parameter_feasibility_20
            + self.chemistry_model_completeness_15
            + self.prommis_idaes_story_fit_10
        )


def candidates() -> list[Candidate]:
    return [
        Candidate(
            rank=2,
            candidate_id="hbta_topo_sulfonated_kerosene_field_water",
            solvent_system="HBTA + TOPO + sulfonated kerosene",
            zotero_keys="JUNBXVTI; 9LJWDC7E; AEL6ZEPG",
            primary_sources=(
                "Gando-Ferreira/Shan 2025 field-water paper; Zhang 2017 "
                "HBTA/TOPO stoichiometry; Zhang 2018 process support"
            ),
            doi_or_url=(
                "10.3390/w17152258; 10.1016/j.seppur.2017.07.028; "
                "10.1016/j.hydromet.2017.10.029"
            ),
            active_status="comparison_and_future_parameterization_lane",
            feed_relevance_20=20,
            extraction_selectivity_20=20,
            non_ionic_realism_15=14,
            epcsaft_parameter_feasibility_20=8,
            chemistry_model_completeness_15=10,
            prommis_idaes_story_fit_10=8,
            evidence_summary=(
                "Only candidate with actual oil-and-gas field-water extraction "
                "evidence plus conventional non-ionic ligand chemistry. The "
                "repo has a source-regressed Li/Na staged model and IDAES "
                "costing handoff, but this is no longer the active flagship "
                "bridge for the Phase 0-9 TEA story. "
                "Zhang 2017 supports 2 HBTA : 1 TOPO : 1 Li stoichiometry; "
                "Zhang 2018 supports multistage HBTA/TOPO/kerosene operation."
            ),
            modeling_status=(
                "source-regressed Li/Na reactive-stage model with ePC-SAFT "
                "aqueous activity support when available; divalent ions are "
                "treated as pretreated feed-context species"
            ),
            best_available_run=(
                "uv run python scripts\\case_study\\hbta_topo_reactive_stage_solve.py"
            ),
            run_artifacts=(
                "hbta_topo_reactive_model_report.md; "
                "hbta_topo_reactive_stage_results.csv; "
                "smackover_prommis_transfer_handoff.csv"
            ),
            next_data_needed=(
                "HBTA, TOPO, sulfonated-kerosene/diluent, Li-BTA-TOPO "
                "parameters; binary interactions; "
                "reaction constants or digitized extraction curves for fitting"
            ),
        ),
        Candidate(
            rank=3,
            candidate_id="raiguel_d2ehdtpa_buphen_geothermal",
            solvent_system="D2EHDTPA + BuPhen + octanol modifiers + n-dodecane",
            zotero_keys="DQ2M7ZG8",
            primary_sources="Raiguel 2024",
            doi_or_url="10.1039/d4gc04760e",
            active_status="best_non_hbta_backup",
            feed_relevance_20=14,
            extraction_selectivity_20=19,
            non_ionic_realism_15=10,
            epcsaft_parameter_feasibility_20=5,
            chemistry_model_completeness_15=9,
            prommis_idaes_story_fit_10=8,
            evidence_summary=(
                "Strong conventional solvent-extraction selectivity over Na, K, "
                "Mg, and Ca in synthetic geothermal brine. It is a serious "
                "backup chemistry because it directly targets multication brines, "
                "but the ligand/synergist set is less simple than HBTA/TOPO and "
                "is not an oil-and-gas produced-water source."
            ),
            modeling_status=(
                "not runnable with current repo ePC-SAFT parameter inventory; "
                "organic ligand, phenanthroline synergist, modifier, and diluent "
                "parameters are absent"
            ),
            best_available_run="parameter-availability check only",
            run_artifacts="solvent_candidate_run_matrix_2026_05_07.csv",
            next_data_needed=(
                "pure-component parameters or density/vapor-pressure/liquid-density "
                "data for D2EHDTPA, BuPhen, octanol modifiers, and n-dodecane; "
                "extraction-equilibrium curves for apparent reaction constants"
            ),
        ),
        Candidate(
            rank=1,
            candidate_id="rezaee_des_topo_pcsaft_epcsaft_pilot",
            solvent_system="TBAC + decanoic-acid DES + TOPO",
            zotero_keys="3NMV5MF2",
            primary_sources="Rezaee 2026",
            doi_or_url="10.1016/j.fluid.2026.114737",
            active_status="flagship_li_na_bridge",
            feed_relevance_20=14,
            extraction_selectivity_20=15,
            non_ionic_realism_15=8,
            epcsaft_parameter_feasibility_20=20,
            chemistry_model_completeness_15=14,
            prommis_idaes_story_fit_10=10,
            evidence_summary=(
                "Current flagship Li/Na bridge because the paper reports "
                "DES/TOPO/RLi/RNa PC-SAFT-style values, organic binary "
                "interactions, reaction constants, extraction-response targets, "
                "and SI equilibrium-composition rows. The repo now derives "
                "distribution coefficients and Smackover Na/TDS sensitivity "
                "rows for PrOMMiS/IDAES from this source-backed basis."
            ),
            modeling_status=(
                "source-regressed Li/Na distribution bridge with Rezaee parameter "
                "payloads, density-fit smoke, ePC-SAFT electrolyte stability, "
                "bounded LLE diagnostics, and PrOMMiS/IDAES transfer handoff"
            ),
            best_available_run=(
                "uv run python analyses\\rezaee_2026_pcsaft_epcsaft\\scripts\\rezaee_li_na_distribution_bridge.py"
            ),
            run_artifacts=(
                "rezaee_li_na_distribution_coefficients.csv; "
                "rezaee_smackover_tds_na_sensitivity.csv; "
                "rezaee_prommis_idaes_transfer_handoff.csv; "
                "rezaee_idaes_costing_input.csv"
            ),
            next_data_needed=(
                "accepted direct ePC-SAFT LLE phase splits across the surrogate "
                "domain, stronger TDS-dependent electrolyte objective, and "
                "approved DES/TOPO solvent-loss and cost assumptions"
            ),
        ),
        Candidate(
            rank=4,
            candidate_id="tbp_fecl3_high_mg_brine",
            solvent_system="TBP + FeCl3/HCl",
            zotero_keys="V7EN7V3S",
            primary_sources="Kia 2024",
            doi_or_url="10.1007/s11356-024-34617-8",
            active_status="mechanistic_backup",
            feed_relevance_20=10,
            extraction_selectivity_20=16,
            non_ionic_realism_15=7,
            epcsaft_parameter_feasibility_20=7,
            chemistry_model_completeness_15=10,
            prommis_idaes_story_fit_10=7,
            evidence_summary=(
                "Useful non-ionic comparison for high-Mg brines with reported "
                "Li/Mg separation and explicit Fe-chloride extraction chemistry. "
                "It is less attractive for the pitch because it brings acid, "
                "iron handling, third-phase risk, and corrosion/process burdens."
            ),
            modeling_status=(
                "no current repo ePC-SAFT solve; TBP and Fe-complex parameter "
                "payloads are not present in the local parameter inventory"
            ),
            best_available_run="parameter-availability check only",
            run_artifacts="solvent_candidate_run_matrix_2026_05_07.csv",
            next_data_needed=(
                "TBP and Fe/Li chloride complex parameters, extraction-equilibrium "
                "constants, aqueous Fe/chloride speciation basis, and acid/corrosion "
                "cost assumptions"
            ),
        ),
        Candidate(
            rank=5,
            candidate_id="d2ehpa_tbp_shale_produced_water_baseline",
            solvent_system="D2EHPA + TBP",
            zotero_keys="BLUVRJ9Q; W3ELF9TE",
            primary_sources="Jang 2017; Lee 2020",
            doi_or_url="10.1016/j.apgeochem.2017.01.016; 10.1016/j.apgeochem.2020.104571",
            active_status="produced_water_limitation_baseline",
            feed_relevance_20=18,
            extraction_selectivity_20=7,
            non_ionic_realism_15=11,
            epcsaft_parameter_feasibility_20=6,
            chemistry_model_completeness_15=8,
            prommis_idaes_story_fit_10=8,
            evidence_summary=(
                "Real shale-gas produced-water context and useful for showing "
                "why a generic solvent-extraction placeholder is not enough. "
                "The current local script predicts weak Li/Na discrimination and "
                "is best used as a comparison/limitation slide."
            ),
            modeling_status=(
                "fixed-assumption placeholder comparison; not a fitted ePC-SAFT "
                "or reactive LLE model"
            ),
            best_available_run=(
                "uv run python scripts\\lle\\jang_2017_stage2_li_na_tbp_d2ehpa.py "
                "(may be slow; existing output retained if timeout occurs)"
            ),
            run_artifacts=(
                "jang_2017_stage2_li_na_summary.md; "
                "jang_2017_stage2_li_na_summary.csv"
            ),
            next_data_needed=(
                "true D2EHPA, TBP, diluent, acid/base reaction constants, and "
                "produced-water organic-contaminant impacts"
            ),
        ),
    ]


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def run_matrix_rows(items: Iterable[Candidate]) -> list[dict[str, str]]:
    rezaee = read_json(OUT_DIR / "rezaee_2026_epcsaft_phase_equilibrium_smoke.json")
    rows: list[dict[str, str]] = []
    for c in items:
        if c.candidate_id == "hbta_topo_sulfonated_kerosene_field_water":
            rows.append(
                {
                    "candidate_id": c.candidate_id,
                    "run_status": "completed_source_regressed_li_na_model",
                    "model_class": "source-regressed Li/Na reactive-stage model",
                    "primary_command": c.best_available_run,
                    "key_metric": "MS-2 stage-1 Li 47.2846%, Na 0.0131%, S_Li/Na 6840.11; stage-3 costing capped to 97.17%",
                    "package_gap": "organic HBTA/TOPO ePC-SAFT parameters and Li/Na reaction constants missing; divalents assumed pretreated",
                }
            )
        elif c.candidate_id == "raiguel_d2ehdtpa_buphen_geothermal":
            rows.append(
                {
                    "candidate_id": c.candidate_id,
                    "run_status": "blocked_parameter_gap",
                    "model_class": "not executed",
                    "primary_command": "parameter-availability check",
                    "key_metric": "literature selectivity strong; no local ePC-SAFT parameter payload for solvent set",
                    "package_gap": "needs neutral/associating parameter regression and reactive LLE fitting workflow",
                }
            )
        elif c.candidate_id == "rezaee_des_topo_pcsaft_epcsaft_pilot":
            stability = rezaee.get("electrolyte_stability", {})
            lle = rezaee.get("electrolyte_lle", {})
            stability_status = stability.get("status", "unknown")
            stable = stability.get("stable", "unknown")
            min_tpd = stability.get("min_tpd", "unknown")
            lle_status = lle.get("status", "unknown")
            rows.append(
                {
                    "candidate_id": c.candidate_id,
                    "run_status": "completed_flagship_li_na_bridge",
                    "model_class": "Rezaee source-regressed Li/Na distribution bridge with ePC-SAFT diagnostics",
                    "primary_command": c.best_available_run,
                    "key_metric": (
                        "32 distribution rows and 60 Smackover Na/TDS/OA sensitivity rows; "
                        "base MS-2 O/A=1 stage-1 Li 45.37%, Na 8.98%, S_Li/Na 8.42; "
                        "stage-3 Li 83.69%, Na 24.59%; density metric 0.007347; electrolyte stability "
                        f"{stability_status}, stable {stable}, min_tpd {min_tpd}; "
                        f"electrolyte LLE status {lle_status}"
                    ),
                    "package_gap": "accepted direct electrolyte-LLE phase splits and stronger TDS-dependent objective still needed for full predictive closure",
                }
            )
        elif c.candidate_id == "tbp_fecl3_high_mg_brine":
            rows.append(
                {
                    "candidate_id": c.candidate_id,
                    "run_status": "blocked_parameter_gap",
                    "model_class": "not executed",
                    "primary_command": "parameter-availability check",
                    "key_metric": "reported literature high-Mg Li extraction; no local TBP/FeCl3 ePC-SAFT parameter payload",
                    "package_gap": "needs Fe/chloride complex chemistry and TBP/complex parameter fitting",
                }
            )
        elif c.candidate_id == "d2ehpa_tbp_shale_produced_water_baseline":
            rows.append(
                {
                    "candidate_id": c.candidate_id,
                    "run_status": "completed_or_existing_placeholder",
                    "model_class": "fixed-assumption placeholder",
                    "primary_command": c.best_available_run,
                    "key_metric": "existing 10-cycle output about Li 40.13%, Na 38.21%; weak selectivity",
                    "package_gap": "needs true D2EHPA/TBP/diluent parameters and reactive extraction constants",
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_review(items: list[Candidate]) -> None:
    lines = [
        "# Non-Ionic Lithium Solvent-Extraction Candidate Scorecard",
        "",
        "Generated by `scripts/case_study/solvent_candidate_scorecard.py`.",
        "",
        "## Scope",
        "",
        "Ionic-liquid extraction systems are excluded from the active candidate ranking because the current case-study direction treats them as too costly and uncertain for the pitch. Ionic-liquid/ePC-SAFT papers remain useful only as method references for parameter fitting and electrolyte-LLE diagnostics.",
        "",
        "The ranking separates three questions that were previously mixed together:",
        "",
        "1. Is the solvent chemistry source-backed for produced-water lithium recovery?",
        "2. Can the chemistry be run today in this repository?",
        "3. Would a completed ePC-SAFT implementation give PrOMMiS/IDAES better transfer variables than a single source-regressed Li/Na model?",
        "",
        "The priority order is presentation-driven rather than a pure descending numeric score: Rezaee 2026 is now the flagship Li/Na bridge because it has the strongest package-facing parameter, reaction, extraction-response, and equilibrium-composition evidence. HBTA/TOPO remains the best conventional field-water comparison and future parameterization lane.",
        "",
        "## Ranked Candidates",
        "",
        "| Rank | Candidate | Zotero keys | Score | Status | Modeling boundary |",
        "|---:|---|---|---:|---|---|",
    ]
    for c in items:
        lines.append(
            f"| {c.rank} | {c.solvent_system} | `{c.zotero_keys}` | "
            f"{c.total_score_100} | {c.active_status} | {c.modeling_status} |"
        )

    lines += [
        "",
        "## Candidate Notes",
        "",
    ]
    for c in items:
        lines += [
            f"### {c.rank}. {c.solvent_system}",
            "",
            f"- **Sources:** {c.primary_sources}. DOI/URL: `{c.doi_or_url}`.",
            f"- **Evidence summary:** {c.evidence_summary}",
            f"- **Best available run:** `{c.best_available_run}`.",
            f"- **Artifacts:** `{c.run_artifacts}`.",
            f"- **Next data needed:** {c.next_data_needed}",
            "",
        ]

    lines += [
        "## Recommended Presentation Position",
        "",
        "Use Rezaee 2026 DES/TOPO as the flagship Li/Na case-study bridge for the current Phase 0-9 TEA story because it supplies source-backed Li/Na extraction responses, SI equilibrium-composition rows, organic PC-SAFT parameter payloads, binary interactions, and reaction constants. The generated bridge now converts those targets into distribution coefficients, Smackover Na/TDS sensitivity rows, and PrOMMiS/IDAES transfer variables.",
        "",
        "Use HBTA/TOPO/sulfonated kerosene as the comparison and future parameterization lane. It remains important because it has field-water and conventional-ligand relevance, but it should not be the active flagship until the organic pure-component, complex, binary-interaction, and reaction-equilibrium parameter gaps are closed.",
        "",
        "Use D2EHPA/TBP as the limitation baseline: it is produced-water relevant but the local model remains placeholder-heavy and weakly selective. Use TBP/FeCl3 and D2EHDTPA/BuPhen as backup chemistries if HBTA/TOPO parameter fitting stalls.",
        "",
        "## Explicit ePC-SAFT Gap",
        "",
        "The case study is scientifically strongest when it states the remaining gap plainly: the active objective is Li over Na after divalent pretreatment, and the Rezaee bridge is source-regressed and ePC-SAFT-supported rather than a fully accepted direct electrolyte-LLE phase split across the full Smackover surrogate domain.",
        "",
    ]
    REVIEW_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    items = sorted(candidates(), key=lambda c: c.rank)
    score_rows: list[dict[str, object]] = []
    for c in items:
        row = asdict(c)
        row["total_score_100"] = c.total_score_100
        score_rows.append(row)
    write_csv(SCORECARD_CSV, score_rows)
    write_csv(RUN_MATRIX_CSV, run_matrix_rows(items))
    write_review(items)
    print(SCORECARD_CSV)
    print(RUN_MATRIX_CSV)
    print(REVIEW_MD)


if __name__ == "__main__":
    main()


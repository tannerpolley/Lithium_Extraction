from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_JSON = REPO_ROOT / 'data' / 'reference' / 'extraction_models' / 'gando_2025' / 'reactive_selectivity.json'


@dataclass
class SelectiveConfig:
    log10_k_li: float
    log10_k_na: float
    log10_capacity_factor: float
    saltout_gain: float
    saltout_ref_mol_L: float
    saltout_anchor_na_mol_L: float

    @property
    def k_li(self) -> float:
        return 10.0 ** self.log10_k_li

    @property
    def k_na(self) -> float:
        return 10.0 ** self.log10_k_na

    @property
    def capacity_factor(self) -> float:
        return 10.0 ** self.log10_capacity_factor


@dataclass
class SelectiveStageResult:
    li_extracted_mol: float
    na_extracted_mol: float
    li_extraction_pct: float
    na_extraction_pct: float
    li_distribution_ratio: float
    li_na_selectivity: float
    extractant_capacity_mol: float
    saltout_factor: float


@dataclass
class ThreeStageResult:
    li_stage_pct: list[float]
    li_cumulative_pct: list[float]
    na_stage_pct: list[float]
    na_cumulative_pct: list[float]
    li_distribution_ratio: list[float]
    li_na_selectivity: list[float]


MW = {
    'Li+': 6.94e-3,
    'Na+': 22.98976928e-3,
    'K+': 39.0983e-3,
}


def load_selective_config(path: str | Path = DEFAULT_CONFIG_JSON) -> SelectiveConfig:
    payload = json.loads(Path(path).read_text(encoding='utf-8'))
    params = payload['parameters']
    constants = payload.get('constants', {})
    return SelectiveConfig(
        log10_k_li=float(params['log10_k_li']),
        log10_k_na=float(params['log10_k_na']),
        log10_capacity_factor=float(params['log10_capacity_factor']),
        saltout_gain=float(params['saltout_gain']),
        saltout_ref_mol_L=float(params['saltout_ref_mol_L']),
        saltout_anchor_na_mol_L=mg_L_to_mol_L(float(constants.get('saltout_anchor_na_mg_L', 10900.0)), 'Na+'),
    )


def mg_L_to_mol_L(value_mg_L: float, species: str) -> float:
    return float(value_mg_L) * 1e-6 / MW[species]


def solve_selective_stage(
    *,
    li_mol_L: float,
    na_mol_L: float,
    top_mol_L: float,
    o_to_a_ratio: float,
    config: SelectiveConfig,
) -> SelectiveStageResult:
    li_mol = max(float(li_mol_L), 0.0)
    na_mol = max(float(na_mol_L), 0.0)
    extractant_capacity_mol = config.capacity_factor * max(float(top_mol_L), 0.0) * max(float(o_to_a_ratio), 0.0)

    if na_mol <= 0.0:
        saltout_factor = 1.0
    else:
        anchor = max(config.saltout_anchor_na_mol_L, 1e-30)
        ref = max(config.saltout_ref_mol_L, 1e-30)
        normalized = np.log1p(na_mol / ref) / np.log1p(anchor / ref)
        saltout_factor = 1.0 + config.saltout_gain * normalized

    w_li = config.k_li * saltout_factor * li_mol
    w_na = config.k_na * na_mol
    denom = 1.0 + w_li + w_na

    li_extracted = min(li_mol * 0.999999, extractant_capacity_mol * w_li / denom)
    na_capacity_remaining = max(0.0, extractant_capacity_mol - li_extracted)
    na_extracted = min(na_mol * 0.999999, na_capacity_remaining * w_na / max(1.0 + w_na, 1e-30))

    li_raff = max(li_mol - li_extracted, 1e-30)
    na_raff = max(na_mol - na_extracted, 1e-30)
    li_org = max(li_extracted, 0.0)
    na_org = max(na_extracted, 0.0)

    li_distribution_ratio = li_org / li_raff
    li_na_selectivity = (li_org / li_raff) / max(na_org / na_raff, 1e-30)

    return SelectiveStageResult(
        li_extracted_mol=li_extracted,
        na_extracted_mol=na_extracted,
        li_extraction_pct=100.0 * li_extracted / max(li_mol, 1e-30),
        na_extraction_pct=100.0 * na_extracted / max(na_mol, 1e-30),
        li_distribution_ratio=li_distribution_ratio,
        li_na_selectivity=li_na_selectivity,
        extractant_capacity_mol=extractant_capacity_mol,
        saltout_factor=float(saltout_factor),
    )


def run_three_stage_crossflow(
    *,
    li_mg_L: float,
    na_mg_L: float,
    top_mol_L: float,
    o_to_a_ratio: float,
    config: SelectiveConfig,
    n_stages: int = 3,
) -> ThreeStageResult:
    li_remaining = mg_L_to_mol_L(li_mg_L, 'Li+')
    na_remaining = mg_L_to_mol_L(na_mg_L, 'Na+')
    li_initial = li_remaining
    na_initial = na_remaining

    li_stage_pct: list[float] = []
    li_cumulative_pct: list[float] = []
    na_stage_pct: list[float] = []
    na_cumulative_pct: list[float] = []
    li_distribution_ratio: list[float] = []
    li_na_selectivity: list[float] = []

    for _ in range(int(n_stages)):
        stage = solve_selective_stage(
            li_mol_L=li_remaining,
            na_mol_L=na_remaining,
            top_mol_L=top_mol_L,
            o_to_a_ratio=o_to_a_ratio,
            config=config,
        )
        li_remaining = max(li_remaining - stage.li_extracted_mol, 0.0)
        na_remaining = max(na_remaining - stage.na_extracted_mol, 0.0)

        li_stage_pct.append(stage.li_extraction_pct)
        na_stage_pct.append(stage.na_extraction_pct)
        li_cumulative_pct.append(100.0 * (1.0 - li_remaining / max(li_initial, 1e-30)))
        na_cumulative_pct.append(100.0 * (1.0 - na_remaining / max(na_initial, 1e-30)))
        li_distribution_ratio.append(stage.li_distribution_ratio)
        li_na_selectivity.append(stage.li_na_selectivity)

    return ThreeStageResult(
        li_stage_pct=li_stage_pct,
        li_cumulative_pct=li_cumulative_pct,
        na_stage_pct=na_stage_pct,
        na_cumulative_pct=na_cumulative_pct,
        li_distribution_ratio=li_distribution_ratio,
        li_na_selectivity=li_na_selectivity,
    )


def load_payload(path: str | Path = DEFAULT_CONFIG_JSON) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding='utf-8'))


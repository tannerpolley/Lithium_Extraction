"""Build a Zotero-derived deep review for lithium solvent-extraction candidates.

This is the fallback path for the same evidence surfaces used by the Zotero MCP
plugin: Zotero Local API metadata plus the local zotero-local-research retrieval
index. It does not use web search.
"""

from __future__ import annotations

import csv
import json
import sqlite3
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "data" / "reference" / "produced_water"
API_BASE = "http://localhost:23119/api/users/0"
INDEX_DB = Path.home() / "AppData" / "Local" / "zotero-local-codex-plugin" / "index.sqlite"
LITHIUM_RECOVERY_COLLECTION = "SAVYNVAK"

COLLECTION_INVENTORY_CSV = OUT_DIR / "zotero_lithium_recovery_collection_inventory_2026_05_07.csv"
EVIDENCE_CSV = OUT_DIR / "zotero_lithium_recovery_api_evidence_2026_05_07.csv"
CANDIDATE_CSV = OUT_DIR / "zotero_lithium_recovery_candidate_expansion_2026_05_07.csv"
PARAMETER_CSV = OUT_DIR / "zotero_lithium_recovery_parameter_fit_opportunities_2026_05_07.csv"
FIGURE_CSV = OUT_DIR / "zotero_lithium_recovery_figure_replication_opportunities_2026_05_07.csv"
REPORT_MD = OUT_DIR / "zotero_lithium_recovery_deep_review_2026_05_07.md"


@dataclass(frozen=True)
class Candidate:
    rank: int
    candidate_id: str
    solvent_set: str
    zotero_keys: str
    status: str
    chemistry_class: str
    feed_relevance: str
    evidence_strength_20: int
    selectivity_strength_20: int
    parameter_fit_potential_20: int
    epcsaft_readiness_20: int
    prommis_idaes_fit_20: int
    best_use: str
    key_data_to_extract: str
    current_limitation: str
    search_terms: tuple[str, ...]

    @property
    def total_score(self) -> int:
        return (
            self.evidence_strength_20
            + self.selectivity_strength_20
            + self.parameter_fit_potential_20
            + self.epcsaft_readiness_20
            + self.prommis_idaes_fit_20
        )


def api_get(path: str, params: dict[str, Any] | None = None) -> Any:
    query = urllib.parse.urlencode(params or {})
    url = f"{API_BASE}{path}" + (f"?{query}" if query else "")
    with urllib.request.urlopen(url, timeout=20) as handle:
        return json.load(handle)


def paged_api_get(path: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    start = 0
    while True:
        page_params = {"limit": 100, "start": start}
        page_params.update(params or {})
        page = api_get(path, page_params)
        if not page:
            return out
        out.extend(page)
        if len(page) < 100:
            return out
        start += 100


def collection_descendants(root_key: str) -> list[str]:
    collections = paged_api_get("/collections")
    children: dict[str, list[str]] = {}
    names: dict[str, str] = {}
    for collection in collections:
        data = collection.get("data", {})
        key = collection["key"]
        names[key] = data.get("name", "")
        parent = data.get("parentCollection") or ""
        children.setdefault(parent, []).append(key)

    ordered: list[str] = []
    stack = [root_key]
    while stack:
        key = stack.pop(0)
        ordered.append(key)
        stack[0:0] = children.get(key, [])
    return ordered


def items_in_collections(collection_keys: list[str]) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    for key in collection_keys:
        for item in paged_api_get(f"/collections/{key}/items", {"include": "data"}):
            data = item.get("data", {})
            if data.get("itemType") in {"attachment", "note"}:
                continue
            items[item["key"]] = item
    return items


def item_meta(item_key: str, collection_items: dict[str, dict[str, Any]]) -> dict[str, str]:
    item = collection_items.get(item_key)
    if item is None:
        try:
            item = api_get(f"/items/{item_key}", {"include": "data"})
        except Exception:
            return {
                "item_key": item_key,
                "title": "not_found",
                "year": "",
                "doi": "",
                "creators": "",
                "publication": "",
            }
    data = item.get("data", {})
    creators = []
    for creator in data.get("creators", []) or []:
        last = creator.get("lastName") or ""
        first = creator.get("firstName") or ""
        creators.append((last if last else first).strip())
    return {
        "item_key": item_key,
        "title": data.get("title", ""),
        "year": str(data.get("date", ""))[:4],
        "doi": data.get("DOI", "") or data.get("doi", ""),
        "creators": "; ".join(c for c in creators if c),
        "publication": data.get("publicationTitle", ""),
    }


def fts_search(query: str, *, item_key: str | None = None, limit: int = 5) -> list[dict[str, str]]:
    if not INDEX_DB.exists():
        return []
    sql = """
        SELECT f.item_key, f.attachment_key, f.title, c.year, f.creators_display, f.doi,
               c.page_label, c.chunk_id,
               snippet(zotero_chunks_fts, 7, '[', ']', ' ... ', 35) AS snippet,
               bm25(zotero_chunks_fts) AS score
        FROM zotero_chunks_fts f
        LEFT JOIN zotero_chunks c ON c.chunk_id = f.chunk_id
        WHERE zotero_chunks_fts MATCH ?
    """
    params: list[Any] = [query]
    if item_key:
        sql += " AND f.item_key = ?"
        params.append(item_key)
    sql += " ORDER BY score LIMIT ?"
    params.append(limit)
    try:
        con = sqlite3.connect(INDEX_DB)
        con.row_factory = sqlite3.Row
        rows = [dict(row) for row in con.execute(sql, params)]
        con.close()
        return [
            {
                key: "" if value is None else str(value)
                for key, value in row.items()
            }
            for row in rows
        ]
    except sqlite3.Error:
        return []


def candidates() -> list[Candidate]:
    return [
        Candidate(
            1,
            "hbta_topo_sulfonated_kerosene",
            "HBTA + TOPO + sulfonated kerosene",
            "JUNBXVTI; 9LJWDC7E; AEL6ZEPG",
            "flagship",
            "beta-diketone/phosphine-oxide synergistic solvent extraction",
            "actual oil-and-gas field water plus alkaline-brine mechanism support",
            20,
            19,
            18,
            11,
            20,
            "Main Friday case study and current source-regressed Li/Na stage model.",
            "Zhang 2017 direct D_Li/D_Na table, pH/temperature/OA curves, Gando Table 2/4/5, Zhang 2018 mixer-settler data.",
            "Organic ePC-SAFT parameters and true reaction constants remain absent.",
            ("HBTA TOPO lithium", "separation factor HBTA TOPO", "distribution ratio HBTA TOPO"),
        ),
        Candidate(
            2,
            "d2ehdtpa_buphen_octanol_dodecane",
            "D2EHDTPA + BuPhen + octanol modifiers + n-dodecane",
            "DQ2M7ZG8",
            "best_non_hbta_multication_backup",
            "cation exchanger plus lithium-selective neutral ligand",
            "synthetic geothermal brine with Na/K/Mg/Ca competition",
            17,
            20,
            14,
            6,
            16,
            "Best backup for multication selectivity and divalent competition story.",
            "Li/Na, Li/K, Li/Mg, Li/Ca separation factors, BuPhen/D2EHDTPA concentration sweeps, van't Hoff fit.",
            "Pure-component and organic-mixture parameters are not available in the repo.",
            ("D2EHDTPA BuPhen lithium", "separation factors lithium magnesium calcium"),
        ),
        Candidate(
            3,
            "rezaee_des_topo",
            "TBAC + decanoic-acid DES + TOPO",
            "3NMV5MF2",
            "parameter_regression_pilot",
            "DES/TOPO with PC-SAFT organic phase and ePC-SAFT aqueous phase",
            "synthetic brine",
            15,
            13,
            20,
            15,
            13,
            "Best source for demonstrating parameter-regression and package plumbing.",
            "DES density correlation, PC-SAFT parameters, binary interactions, extraction-isotherm tables.",
            "Not the flagship HBTA/TOPO chemistry and direct LLE smoke remains diagnostic.",
            ("Rezaee TOPO PC-SAFT lithium", "deep eutectic TOPO lithium"),
        ),
        Candidate(
            4,
            "tbp_fecl3_hcl",
            "TBP + FeCl3/HCl + kerosene",
            "V7EN7V3S; UBWCFMKD",
            "conventional_high_mg_backup",
            "organophosphorus/chloroferrate extraction chemistry",
            "high Mg/Li brines",
            14,
            17,
            12,
            7,
            12,
            "Useful conventional comparator if HBTA/TOPO parameterization stalls.",
            "Fe/Li, HCl, TBP interactions; Li/Mg separation; third-phase/solvent-loss limits.",
            "Acid/Fe handling, corrosion, and chloride speciation complicate IDAES story.",
            ("TBP FeCl3 lithium", "high magnesium brine lithium TBP"),
        ),
        Candidate(
            5,
            "d2ehpa_tbp_produced_water",
            "D2EHPA + TBP + kerosene",
            "BLUVRJ9Q; W3ELF9TE",
            "produced_water_limitation_baseline",
            "acidic organophosphorus extraction",
            "synthetic shale-gas produced water and organic-contaminant follow-up",
            18,
            8,
            11,
            7,
            15,
            "Limitation baseline showing why generic solvent extraction is not enough.",
            "Stage-1 divalent removal, Li loss, organic-contaminant impact, TBP/D2EHPA concentration curves.",
            "Low Li recovery/selectivity relative to flagship; current model is placeholder-heavy.",
            ("D2EHPA TBP lithium", "produced water lithium solvent extraction"),
        ),
        Candidate(
            6,
            "hbta_topo_des_hanada",
            "HBTA/TOPO or HTTA/TOPO synergistic DES",
            "GK598336",
            "new_candidate_physical_property_fit",
            "solvent-free beta-diketone/phosphine-oxide DES",
            "model brine",
            13,
            15,
            18,
            10,
            11,
            "New candidate for pseudo-component physical-property fitting and capacity comparison.",
            "DES density/viscosity, Li capacity, Li/Na/K selectivity, HBTA/TOPO physical properties.",
            "DES cost/viscosity and chemistry differ from sulfonated-kerosene flagship.",
            ("Synergistic Deep Eutectic Solvents lithium TOPO", "HBTA TOPO DES lithium"),
        ),
        Candidate(
            7,
            "functional_ionic_liquid_produced_water",
            "functional ionic liquids for Canadian oil-and-gas produced water",
            "6TD5NWA8",
            "new_candidate_produced_water_alternate",
            "functional ionic-liquid extraction",
            "real Canadian oil-and-gas produced water",
            18,
            13,
            9,
            8,
            11,
            "New alternate because it uses real produced-water samples; keep outside flagship cost story.",
            "Real-water composition, Li recovery/selectivity, extractant loss, viscosity/cost constraints.",
            "Ionic-liquid cost/uncertainty conflicts with current non-ionic pitch.",
            ("functional ionic liquids produced water lithium", "Canadian oil gas produced water lithium"),
        ),
        Candidate(
            8,
            "heteropolyacid_ionic_liquid",
            "heteropolyacid ionic liquid + hydrophobic ionic-liquid diluent",
            "5DXFW24T",
            "new_candidate_high_mg_selectivity",
            "heteropolyacid ionic-liquid extraction",
            "high Mg/Li salt-lake brine",
            11,
            16,
            11,
            8,
            10,
            "New high-Mg selectivity candidate and mechanistic contrast to TBP/FeCl3.",
            "Li/Mg selectivity, organic composition, stripping, cyclic stability, extraction constants if tabulated.",
            "Not produced-water specific and not aligned with non-ionic flagship.",
            ("heteropolyacid lithium high magnesium brine", "recovery lithium ions salt lake brine heteropolyacid"),
        ),
        Candidate(
            9,
            "ammonium_ionic_liquid",
            "ammonium ionic liquid extraction system",
            "EQG5BQQV",
            "new_candidate_ionic_liquid_reference",
            "ammonium ionic-liquid extraction",
            "aqueous solution/model brine",
            10,
            12,
            10,
            8,
            8,
            "Mechanism and cost-bound reference for why ionic-liquid systems are not the active pitch.",
            "Distribution ratios, stripping, cation/anion structure, solvent loss and reuse.",
            "Lower fit priority than HBTA/TOPO, Raiguel, or Rezaee for Friday.",
            ("ammonium ionic liquid lithium extraction", "ionic liquid lithium aqueous solution"),
        ),
        Candidate(
            10,
            "dbm_topo_review_only",
            "DBM + TOPO synergistic extraction",
            "5HLW3Y8W",
            "review_only_primary_needed",
            "beta-diketone/phosphine-oxide synergistic solvent extraction",
            "review reports actual UOG brine; primary record not yet pinned in Zotero",
            10,
            17,
            12,
            8,
            11,
            "High-upside historical target if the primary paper/data table can be pinned.",
            "Primary-paper D values, Li/Na ratio, O/A, extractant concentration, stripping, and brine composition.",
            "Current support is review-derived; do not promote into the deck until the primary source is identified.",
            ("DBM TOPO lithium", "dibenzoylmethane TOPO lithium extraction"),
        ),
    ]


def parameter_opportunities() -> list[dict[str, str]]:
    return [
        {
            "priority": "1",
            "zotero_keys": "9LJWDC7E",
            "source": "Zhang 2017 HBTA/TOPO",
            "fit_opportunity": "Replace derived Na anchor with direct D_Li=33.7 and D_Na=0.016 table plus capacity/OA/temperature points.",
            "expected_score_gain": "Raises distribution treatment, parameter identifiability, and physicality.",
            "implementation": "Digitize or table-extract figures/tables, then refit hbta_topo_reactive_stage_solve.py targets.",
        },
        {
            "priority": "2",
            "zotero_keys": "JUNBXVTI",
            "source": "Gando/Shan 2025 field water",
            "fit_opportunity": "Use Table 2 cation effects and Table 4 staged extraction as separated pretreatment/stage validation data.",
            "expected_score_gain": "Improves divalent assumption and stage validation confidence.",
            "implementation": "Store Table 2 cation impact rows and fit/validate only Li/Na unless divalent data are adequate.",
        },
        {
            "priority": "3",
            "zotero_keys": "AEL6ZEPG",
            "source": "Zhang 2018 mixer-settler",
            "fit_opportunity": "Use 7-stage/30 h mixer-settler data as process-scale validation, not parameter fitting.",
            "expected_score_gain": "Improves PrOMMiS staged-unit credibility.",
            "implementation": "Add process validation rows and compare model stage count/recovery/concentration to reported operation.",
        },
        {
            "priority": "4",
            "zotero_keys": "DQ2M7ZG8",
            "source": "Raiguel 2024",
            "fit_opportunity": "Extract multication selectivity and van't Hoff trends for backup chemistry.",
            "expected_score_gain": "Improves backup selectivity and divalent-competition benchmark.",
            "implementation": "Create a parameter-inventory gap table for D2EHDTPA/BuPhen/octanol/n-dodecane.",
        },
        {
            "priority": "5",
            "zotero_keys": "3NMV5MF2; GK598336",
            "source": "Rezaee 2026 and Hanada 2021",
            "fit_opportunity": "Use DES density/PC-SAFT-style data for pseudo-component regression smoke tests.",
            "expected_score_gain": "Improves package-method confidence but not flagship chemistry completeness.",
            "implementation": "Keep Rezaee smoke test; add Hanada DES as an optional pseudo-component fit if density/viscosity tables are extractable.",
        },
    ]


def figure_opportunities() -> list[dict[str, str]]:
    return [
        {
            "article": "Yu 2024",
            "current_artifact": "scripts/Yu_2024_analysis/output/yu_2024_figure6_reactive_replication.png",
            "status": "existing_recreation_and_package_diagnostic",
            "next_action": "Re-run digitized and reactive scripts; keep direct ePC-SAFT collapse as diagnostic if it remains.",
        },
        {
            "article": "Hubach 2024",
            "current_artifact": "data/multiphase/hubach_2024_figure7_replication.png",
            "status": "existing_replication_with_native_ePC-SAFT_failure_diagnostics",
            "next_action": "Run bounded single-point checks only; full run can hang.",
        },
        {
            "article": "Gando/Shan 2025",
            "current_artifact": "data/multiphase/gando_2025_slide_assets/gando_2025_stagewise_extraction_bars.png",
            "status": "existing selective-stage assets and source-regressed HBTA/TOPO model",
            "next_action": "Add Zhang 2017 D/isotherm data before changing the fit.",
        },
        {
            "article": "Jang 2017",
            "current_artifact": "data/multiphase/jang_2017_stage2_li_na_efficiency_plot.png",
            "status": "existing limitation-baseline output; script may be slow",
            "next_action": "Run with timeout; retain existing output if it exceeds practical runtime.",
        },
        {
            "article": "Zhang 2017",
            "current_artifact": "not_yet_digitized",
            "status": "highest_value_new_figure_target",
            "next_action": "Digitize pH, O/A/isotherm, and temperature plots to improve HBTA/TOPO fit.",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    collection_keys = collection_descendants(LITHIUM_RECOVERY_COLLECTION)
    collection_items = items_in_collections(collection_keys)
    collection_rows = []
    for item in collection_items.values():
        data = item.get("data", {})
        collection_rows.append(
            {
                "item_key": item["key"],
                "title": data.get("title", ""),
                "date": data.get("date", ""),
                "doi": data.get("DOI", ""),
                "item_type": data.get("itemType", ""),
                "collections": ";".join(data.get("collections", []) or []),
                "source": "zotero_local_api_lithium_recovery_recursive",
            }
        )
    collection_rows.sort(key=lambda row: (row["date"], row["title"]), reverse=True)
    write_csv(COLLECTION_INVENTORY_CSV, collection_rows)

    candidate_rows: list[dict[str, Any]] = []
    evidence_rows: list[dict[str, Any]] = []
    for candidate in candidates():
        keys = [key.strip() for key in candidate.zotero_keys.split(";") if key.strip()]
        metas = [item_meta(key, collection_items) for key in keys]
        candidate_rows.append(
            {
                "rank": candidate.rank,
                "candidate_id": candidate.candidate_id,
                "solvent_set": candidate.solvent_set,
                "zotero_keys": candidate.zotero_keys,
                "titles": " | ".join(meta["title"] for meta in metas),
                "dois": " | ".join(meta["doi"] for meta in metas),
                "status": candidate.status,
                "chemistry_class": candidate.chemistry_class,
                "feed_relevance": candidate.feed_relevance,
                "evidence_strength_20": candidate.evidence_strength_20,
                "selectivity_strength_20": candidate.selectivity_strength_20,
                "parameter_fit_potential_20": candidate.parameter_fit_potential_20,
                "epcsaft_readiness_20": candidate.epcsaft_readiness_20,
                "prommis_idaes_fit_20": candidate.prommis_idaes_fit_20,
                "total_score_100": candidate.total_score,
                "best_use": candidate.best_use,
                "key_data_to_extract": candidate.key_data_to_extract,
                "current_limitation": candidate.current_limitation,
                "evidence_source": "fresh_zotero_mcp_verified; current_thread_fallback_zotero_local_api_plus_local_retrieval_index",
            }
        )
        for query in candidate.search_terms:
            hits = fts_search(query, limit=4)
            for hit in hits:
                evidence_rows.append(
                    {
                        "candidate_id": candidate.candidate_id,
                        "query": query,
                        "item_key": hit["item_key"],
                        "title": hit["title"],
                        "year": hit["year"],
                        "doi": hit["doi"],
                        "chunk_id": hit["chunk_id"],
                        "page_label": hit["page_label"],
                        "snippet": " ".join(hit["snippet"].split()),
                        "source": "zotero_local_retrieval_index_fts",
                    }
                )
    write_csv(CANDIDATE_CSV, candidate_rows)
    write_csv(EVIDENCE_CSV, evidence_rows)
    write_csv(PARAMETER_CSV, parameter_opportunities())
    write_csv(FIGURE_CSV, figure_opportunities())

    top_candidates = sorted(candidate_rows, key=lambda row: int(row["total_score_100"]), reverse=True)
    lines = [
        "# Zotero Lithium Recovery Deep Review",
        "",
        "Generated by `scripts/case_study/zotero_lithium_recovery_deep_review.py` using Zotero Local API metadata and the local zotero-local-research retrieval index. No web search fallback is used.",
        "",
        "The current thread's Zotero MCP transport returned `Transport closed` after the required single lightweight retry. A fresh subagent verified that the Zotero MCP plugin itself works against the same library and returned the Lithium Recovery collection key `SAVYNVAK`; therefore the rows below are labeled as Zotero-derived API/index fallback evidence, not as successful current-thread MCP calls.",
        "",
        "## Access Parity",
        "",
        f"- Lithium Recovery collection key: `{LITHIUM_RECOVERY_COLLECTION}`.",
        f"- Recursive Zotero Local API item count captured in this script: `{len(collection_rows)}`.",
        "- Fresh Zotero MCP subagent check returned `45` recursive collection item briefs and direct item count `30`.",
        f"- Local retrieval index path: `{INDEX_DB}`.",
        "- Evidence snippets are from indexed Zotero chunks, matching the data surface used by the Zotero plugin retrieval tools.",
        "",
        "## Best Candidate Solvent Sets",
        "",
        "| Evidence priority | Solvent set | Status | Score | Best use | Main limitation |",
        "|---:|---|---|---:|---|---|",
    ]
    for row in top_candidates:
        lines.append(
            f"| {row['rank']} | {row['solvent_set']} | {row['status']} | {row['total_score_100']} | "
            f"{row['best_use']} | {row['current_limitation']} |"
        )
    lines.extend(
        [
            "",
            "## Highest-Value Fit Improvements",
            "",
            "| Priority | Source | Fit opportunity | Implementation |",
            "|---:|---|---|---|",
        ]
    )
    for row in parameter_opportunities():
        lines.append(
            f"| {row['priority']} | {row['source']} (`{row['zotero_keys']}`) | "
            f"{row['fit_opportunity']} | {row['implementation']} |"
        )
    lines.extend(
        [
            "",
            "## Figure And Analysis Revalidation Targets",
            "",
            "| Article | Current artifact | Status | Next action |",
            "|---|---|---|---|",
        ]
    )
    for row in figure_opportunities():
        lines.append(
            f"| {row['article']} | `{row['current_artifact']}` | {row['status']} | {row['next_action']} |"
        )
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            "Zhang 2017 remains the highest-value immediate upgrade for the flagship HBTA/TOPO case because it adds direct distribution-ratio, O/A, capacity, and temperature data to the current Gando-stage recovery anchors. Raiguel 2024 is the best non-HBTA multication backup. Rezaee 2026 and Hanada 2021 are useful parameter-regression/pseudo-component pilots. Ionic-liquid produced-water systems should be kept as alternate evidence, not the Friday flagship, unless cost and viscosity assumptions are explicitly defended.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"Saved {COLLECTION_INVENTORY_CSV}")
    print(f"Saved {CANDIDATE_CSV}")
    print(f"Saved {EVIDENCE_CSV}")
    print(f"Saved {PARAMETER_CSV}")
    print(f"Saved {FIGURE_CSV}")
    print(f"Saved {REPORT_MD}")


if __name__ == "__main__":
    main()


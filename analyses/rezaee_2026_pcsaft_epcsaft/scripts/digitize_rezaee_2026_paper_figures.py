from __future__ import annotations

import csv
import json
import urllib.request
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

ANALYSIS_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ANALYSIS_DIR / "data" / "processed"
RESULTS_DIR = ANALYSIS_DIR / "results" / "reaction_equilibrium"
DIGITIZATION_DIR = RESULTS_DIR / "figure_digitization"
SOURCE_DIR = DIGITIZATION_DIR / "source_images"
OVERLAY_DIR = DIGITIZATION_DIR / "overlays"

DIGITIZED_CSV = PROCESSED_DIR / "rezaee_2026_paper_figure_digitized_points.csv"
SUMMARY_JSON = RESULTS_DIR / "rezaee_2026_paper_figure_digitization_summary.json"
REPORT_MD = RESULTS_DIR / "rezaee_2026_paper_figure_digitization.md"

FIGURE_SPECS: list[dict[str, Any]] = [
    {
        "figure_id": "fig7",
        "paper_label": "Fig. 7",
        "axis_max": 60.0,
        "caption": "Deviation of calculated extraction percentage from experimental data [17].",
        "source_name": "fig7_source.jpg",
        "source_url": (
            "https://cdn.mathpix.com/cropped/93f7cf5c-3cc6-42a8-8ff1-401396fd69cc-09.jpg"
            "?height=871&width=1147&top_left_y=185&top_left_x=460"
        ),
    },
    {
        "figure_id": "fig8",
        "paper_label": "Fig. 8",
        "axis_max": 6.0,
        "caption": "Deviation of calculated selectivity from experimental data [17].",
        "source_name": "fig8_source.jpg",
        "source_url": (
            "https://cdn.mathpix.com/cropped/93f7cf5c-3cc6-42a8-8ff1-401396fd69cc-09.jpg"
            "?height=882&width=1140&top_left_y=1177&top_left_x=465"
        ),
    },
    {
        "figure_id": "fig10",
        "paper_label": "Fig. 10",
        "axis_max": 60.0,
        "caption": "Deviation of calculated lithium extraction percentage from experimental data [17] using $k_{ij}$.",
        "source_name": "fig10_source.jpg",
        "source_url": (
            "https://cdn.mathpix.com/cropped/93f7cf5c-3cc6-42a8-8ff1-401396fd69cc-11.jpg"
            "?height=864&width=1133&top_left_y=189&top_left_x=467"
        ),
    },
    {
        "figure_id": "fig11",
        "paper_label": "Fig. 11",
        "axis_max": 6.0,
        "caption": "Deviation of calculated selectivity from experimental data [17] using $k_{ij}$.",
        "source_name": "fig11_source.jpg",
        "source_url": (
            "https://cdn.mathpix.com/cropped/93f7cf5c-3cc6-42a8-8ff1-401396fd69cc-11.jpg"
            "?height=882&width=1140&top_left_y=1179&top_left_x=465"
        ),
    },
]


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


def _download_if_missing(spec: dict[str, Any]) -> Path:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    out = SOURCE_DIR / str(spec["source_name"])
    if out.exists():
        return out
    urllib.request.urlretrieve(str(spec["source_url"]), out)
    return out


def _red_mask(image: np.ndarray) -> np.ndarray:
    return (image[:, :, 0] > 180) & (image[:, :, 1] < 120) & (image[:, :, 2] < 120)


def _black_mask(image: np.ndarray) -> np.ndarray:
    return (image[:, :, 0] < 80) & (image[:, :, 1] < 80) & (image[:, :, 2] < 80)


def _line_calibration(image: np.ndarray) -> dict[str, float]:
    red = _red_mask(image)
    ys, xs = np.where(red)
    if len(xs) == 0:
        raise ValueError("No red 1:1 line pixels found in source image")
    slope, intercept = np.polyfit(xs.astype(float), ys.astype(float), deg=1)
    x_min = float(xs.min())
    x_max = float(xs.max())
    return {
        "x_min": x_min,
        "x_max": x_max,
        "y_at_x_min": float(slope * x_min + intercept),
        "y_at_x_max": float(slope * x_max + intercept),
        "slope": float(slope),
        "intercept": float(intercept),
    }


def _component_points(region: np.ndarray) -> list[tuple[float, float]]:
    area = int(region.sum())
    if area < 120:
        return []
    ys, xs = np.where(region)
    height = int(ys.max() - ys.min() + 1)
    width = int(xs.max() - xs.min() + 1)
    if area <= 500 and 14 <= width <= 28 and 14 <= height <= 28:
        cy, cx = ndi.center_of_mass(region)
        return [(float(cx), float(cy))]

    dist = ndi.distance_transform_edt(region)
    peaks = (dist == ndi.maximum_filter(dist, size=15)) & (dist > 7.5)
    peak_labels, peak_count = ndi.label(peaks)
    if peak_count == 0:
        cy, cx = ndi.center_of_mass(region)
        return [(float(cx), float(cy))]
    return [(float(cx), float(cy)) for cy, cx in ndi.center_of_mass(peaks, peak_labels, range(1, peak_count + 1))]


def _digitize_points(image: np.ndarray, calibration: dict[str, float]) -> list[tuple[float, float]]:
    x_min = int(round(calibration["x_min"]))
    x_max = int(round(calibration["x_max"]))
    y_top = int(round(calibration["y_at_x_max"]))
    y_bottom = int(round(calibration["y_at_x_min"]))

    left = max(x_min + 50, 0)
    right = min(x_max - 40, image.shape[1])
    top = max(y_top - 10, 0)
    bottom = min(y_bottom + 10, image.shape[0])

    roi = image[top:bottom, left:right]
    black = _black_mask(roi)
    labels, count = ndi.label(black)
    slices = ndi.find_objects(labels)

    points: list[tuple[float, float]] = []
    for label_id, slc in enumerate(slices, start=1):
        if slc is None:
            continue
        region = labels[slc] == label_id
        for cx, cy in _component_points(region):
            points.append((left + slc[1].start + cx, top + slc[0].start + cy))
    return sorted(points, key=lambda item: (item[0], item[1]))


def _pixel_to_data(px: float, py: float, calibration: dict[str, float], axis_max: float) -> tuple[float, float]:
    x_value = axis_max * (px - calibration["x_min"]) / max(calibration["x_max"] - calibration["x_min"], 1.0)
    y_value = axis_max * (calibration["y_at_x_min"] - py) / max(
        calibration["y_at_x_min"] - calibration["y_at_x_max"],
        1.0,
    )
    return float(x_value), float(y_value)


def _overlay_image(source: Path, points: list[tuple[float, float]], overlay: Path) -> None:
    image = Image.open(source).convert("RGB")
    draw = ImageDraw.Draw(image)
    for px, py in points:
        draw.ellipse((px - 5, py - 5, px + 5, py + 5), outline=(255, 255, 0), width=2)
    overlay.parent.mkdir(parents=True, exist_ok=True)
    image.save(overlay)


def _write_report(summary: dict[str, Any]) -> None:
    lines = [
        "# Rezaee 2026 Paper Figure Digitization",
        "",
        "## Scope",
        "",
        "This workflow digitizes the published Figure 7, 8, 10, and 11 scatter panels directly from the paper images.",
        "",
        "The direct source tables in this analysis folder remain useful for literature context, but they do not reconstruct the plotted panels cleanly under one consistent Section 3.2 basis. For figure replication, the digitized panel points are therefore treated as the figure-data source of truth.",
        "",
        "## Results",
        "",
    ]
    for entry in summary["figures"]:
        lines.extend(
            [
                f"- `{entry['paper_label']}` digitized `{entry['row_count']}` points with x-range `{entry['x_min']}` to `{entry['x_max']}` and y-range `{entry['y_min']}` to `{entry['y_max']}`.",
                f"  Source image: `{Path(entry['source_image']).relative_to(ANALYSIS_DIR)}`",
                f"  QA overlay: `{Path(entry['overlay']).relative_to(ANALYSIS_DIR)}`",
            ]
        )
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows: list[dict[str, Any]] = []
    figure_entries: list[dict[str, Any]] = []

    for spec in FIGURE_SPECS:
        source = _download_if_missing(spec)
        image = np.asarray(Image.open(source).convert("RGB"))
        calibration = _line_calibration(image)
        points = _digitize_points(image, calibration)
        overlay = OVERLAY_DIR / f"{spec['figure_id']}_overlay.png"
        _overlay_image(source, points, overlay)

        figure_rows = []
        for px, py in points:
            x_value, y_value = _pixel_to_data(px, py, calibration, float(spec["axis_max"]))
            record = {
                "figure_id": str(spec["figure_id"]),
                "paper_label": str(spec["paper_label"]),
                "caption": str(spec["caption"]),
                "axis_max": float(spec["axis_max"]),
                "x": x_value,
                "y": y_value,
                "pixel_x": float(px),
                "pixel_y": float(py),
                "source_image": str(source),
                "overlay": str(overlay),
            }
            rows.append(record)
            figure_rows.append(record)

        frame = np.asarray([(item["x"], item["y"]) for item in figure_rows], dtype=float)
        figure_entries.append(
            {
                "figure_id": str(spec["figure_id"]),
                "paper_label": str(spec["paper_label"]),
                "row_count": int(len(figure_rows)),
                "source_image": str(source),
                "overlay": str(overlay),
                "axis_max": float(spec["axis_max"]),
                "x_min": float(frame[:, 0].min()) if len(frame) else None,
                "x_max": float(frame[:, 0].max()) if len(frame) else None,
                "y_min": float(frame[:, 1].min()) if len(frame) else None,
                "y_max": float(frame[:, 1].max()) if len(frame) else None,
                "line_calibration": calibration,
            }
        )

    DIGITIZED_CSV.parent.mkdir(parents=True, exist_ok=True)
    with DIGITIZED_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "figure_id",
                "paper_label",
                "caption",
                "axis_max",
                "x",
                "y",
                "pixel_x",
                "pixel_y",
                "source_image",
                "overlay",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "status": "paper_figure_digitization_complete",
        "figure_count": len(figure_entries),
        "digitized_points_csv": str(DIGITIZED_CSV.relative_to(ANALYSIS_DIR)),
        "figures": figure_entries,
    }
    SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_JSON.write_text(json.dumps(_jsonable(summary), indent=2) + "\n", encoding="utf-8")
    _write_report(summary)
    print(json.dumps(_jsonable(summary), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

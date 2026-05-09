from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts._analysis_wrapper import load_or_run

load_or_run(globals(), "analyses.rezaee_2026_pcsaft_epcsaft.scripts.rezaee_des_epcsaft_parameter_smoke")


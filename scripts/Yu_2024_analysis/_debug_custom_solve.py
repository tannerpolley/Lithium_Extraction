from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._analysis_wrapper import load_or_run

load_or_run(globals(), "analyses.yu_2024_figure6.scripts._debug_custom_solve")



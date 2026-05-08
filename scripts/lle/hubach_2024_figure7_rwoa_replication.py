from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._analysis_wrapper import load_or_run

load_or_run(globals(), "analyses.electrolyte_lle_literature.scripts.hubach_2024_figure7_rwoa_replication")



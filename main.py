import runpy
import sys
from pathlib import Path


project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

runpy.run_path(
    str(project_root / "ui" / "ui.py"),
    run_name="__main__"
)
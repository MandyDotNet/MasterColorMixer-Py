# Ensure src/ is on sys.path so we can import master_color_mixer.*
import sys
from pathlib import Path

# project root: tests/.. (parent of tests)
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Put src/ at the front of sys.path
sys.path.insert(0, str(SRC))
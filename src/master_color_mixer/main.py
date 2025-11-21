# Running this module starts the FastAPI app and prints a hello message.
    # Demo added 11/21/2025 for algorithms testing - to be moved to right place next week

#disgusting hack I will remove when more of the app architecture is developed.
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import uvicorn

from master_color_mixer.data.palette_catalog import (
    get_all_colors_sorted,
    add_unlocked_color
    )

def main():
    print("Hello MasterColorMixer (starting API...)")
    uvicorn.run("src.master_color_mixer.app:app", host="127.0.0.1", port=8000, reload=False)

    # Demo added 11/21/2025: 
    # pretend the child has just discovered some colors
    add_unlocked_color("orange")
    add_unlocked_color("purple")

    colors = get_all_colors_sorted()
    print("Loaded colors (sorted):", ", ".join(colors))

if __name__ == "__main__":
    main()
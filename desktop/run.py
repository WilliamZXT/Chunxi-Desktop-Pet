"""Source and PyInstaller entry point. Resolve assets relative to the distribution."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from chunxi.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())

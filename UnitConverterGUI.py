"""PyQt GUI entry point — run: python UnitConverterGUI.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from boundary.qt_app import main  # noqa: E402
except ModuleNotFoundError as exc:
    if exc.name == "PyQt6":
        print(
            "PyQt6가 설치되어 있지 않습니다.\n"
            "  pip install PyQt6\n"
            "또는\n"
            "  pip install -e \".[gui]\""
        )
        sys.exit(1)
    raise


if __name__ == "__main__":
    main()

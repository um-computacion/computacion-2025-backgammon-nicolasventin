"""Configuración común para las pruebas."""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    """Incluye el directorio raíz en sys.path."""
    root = Path(__file__).resolve().parent
    src_path = root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(root))


_ensure_src_on_path()


"""Проверки за задача 4.3: chetim.py прави същото, но се чете.

Пускане:  python -m pytest urok-4-debug-i-git/4.3-preimenuvay -v

Проверките не могат да кажат дали имената са ДОБРИ — това решава
учителят. Те само хващат очевидното: еднобуквени имена, липсващи
docstring-ове и променено поведение.
"""
import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
CHETIM = HERE / "chetim.py"
RAZRESHENI = {"_", "i", "j"}  # броячи в цикли са приемливи


def darvo():
    if not CHETIM.exists():
        pytest.fail("Липсва chetim.py. Създайте го до nechetim.py.")
    return ast.parse(CHETIM.read_text(encoding="utf-8"))


def funktsii(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def pusni(path):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    return subprocess.run([sys.executable, str(path)], cwd=HERE, capture_output=True,
                          text=True, encoding="utf-8", env=env)


def test_sashtiyat_izhod():
    darvo()
    predi, sled = pusni(HERE / "nechetim.py"), pusni(CHETIM)
    assert sled.returncode == 0, sled.stderr
    assert sled.stdout == predi.stdout, "Логиката не бива да се променя: изходът трябва да е същият"


def test_pone_dve_funktsii():
    assert len(funktsii(darvo())) >= 2, "Разделете f на поне две функции"


def test_vsyaka_funktsiya_ima_docstring():
    for fn in funktsii(darvo()):
        assert ast.get_docstring(fn), f"Функцията {fn.name} няма docstring"


def test_nyama_ednobukveni_imena():
    tree = darvo()
    loshi = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and len(node.name) == 1:
            loshi.add(node.name)
        elif isinstance(node, ast.arg) and len(node.arg) == 1:
            loshi.add(node.arg)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and len(node.id) == 1:
            loshi.add(node.id)
    loshi -= RAZRESHENI
    assert not loshi, f"Еднобуквени имена: {', '.join(sorted(loshi))}"

"""Проверки за задача 3.2: правилно ли е разделена програмата?

Пускане:  python -m pytest urok-3-failove-i-moduli/3.2-razglobete-programata -v
"""
import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
MODULES = ["chetene.py", "analiz.py", "main.py"]


def iztochnik(name):
    path = HERE / name
    if not path.exists():
        pytest.fail(f"Липсва файлът {name}. Разделете vsichko.py на {', '.join(MODULES)}.")
    return path.read_text(encoding="utf-8")


def izvikani_funktsii(code):
    """Имената на всички функции, които се извикват в кода."""
    names = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            names.add(node.func.id)
    return names


def pusni(args, cwd):
    env = {**os.environ, "PYTHONPATH": str(HERE), "PYTHONIOENCODING": "utf-8"}
    return subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8", env=env)


@pytest.mark.parametrize("name", MODULES)
def test_modulat_sashtestvuva(name):
    iztochnik(name)


def test_analiz_nyama_open():
    assert "open" not in izvikani_funktsii(iztochnik("analiz.py")), \
        "analiz.py не бива да докосва диска — четенето е работа на chetene.py"


def test_analiz_nyama_print():
    code = iztochnik("analiz.py")
    tree = ast.parse(code)
    # print е позволен само в блока if __name__ == "__main__":
    for node in tree.body:
        if isinstance(node, ast.If) and "__main__" in ast.unparse(node.test):
            continue
        if "print" in izvikani_funktsii(ast.unparse(node)):
            pytest.fail("analiz.py печата извън блока if __name__ == \"__main__\":")


def test_analiz_ima_blok_main():
    assert '__name__ == "__main__"' in iztochnik("analiz.py") or \
           "__name__ == '__main__'" in iztochnik("analiz.py"), \
        "Добавете в analiz.py блок if __name__ == \"__main__\": с 5 проверки"


def test_import_na_analiz_ne_pechata_i_ne_chete(tmp_path):
    iztochnik("analiz.py")
    result = pusni(["-c", "import analiz"], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "", "При import analiz.py не бива да печата нищо"


def test_proverkite_v_analiz_minavat_bez_failove(tmp_path):
    iztochnik("analiz.py")
    result = pusni([str(HERE / "analiz.py")], cwd=tmp_path)
    assert result.returncode == 0, result.stderr


def test_main_dava_sashtiya_izhod_kato_vsichko():
    iztochnik("main.py")
    predi = pusni([str(HERE / "vsichko.py")], cwd=HERE)
    sled = pusni([str(HERE / "main.py")], cwd=HERE)
    assert sled.returncode == 0, sled.stderr
    assert sled.stdout == predi.stdout, \
        "Разделянето не бива да променя поведението: main.py трябва да печата същото като vsichko.py"

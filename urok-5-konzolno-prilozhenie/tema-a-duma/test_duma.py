"""Проверки за тема A: функцията check() от duma.py.

Копирайте този файл в папката на проекта си, до duma.py, и пуснете:
    python -m pytest -v

check(guess, secret) връща списък от "green" / "yellow" / "grey"
за всяка буква на опита.
"""
import pytest

duma = pytest.importorskip("duma", reason="в тази папка няма duma.py — копирайте теста до своя проект")
check = duma.check


def test_primer_ot_uroka():
    assert check("ТОЧКА", "КНИГА") == ["grey", "grey", "grey", "yellow", "green"]


def test_povtaryashti_se_bukvi():
    # В тайната дума има само едно А, затова само първото А в опита е жълто.
    assert check("ААБВГ", "ВГДАБ") == ["yellow", "grey", "yellow", "yellow", "yellow"]


def test_poznata_duma():
    assert check("КНИГА", "КНИГА") == ["green"] * 5


def test_nishto_obshto():
    assert check("ЖИРАФ", "СЛОВО") == ["grey"] * 5


def test_zelenata_bukva_ne_se_broi_vtori_pat_kato_zhalta():
    # П на позиция 0 е жълто (в ЛАМПА има едно П), второто П е сиво.
    assert check("ПАПКА", "ЛАМПА") == ["yellow", "green", "grey", "grey", "green"]


def test_zelenoto_ima_predimstvo_pred_zhaltoto():
    # Последното А е на мястото си. Първото А не бива да „изяде“ това срещане.
    assert check("АБВГА", "ДЕЖЗА") == ["grey", "grey", "grey", "grey", "green"]


def test_vsichki_bukvi_na_greshno_myasto():
    assert check("ЗЕБРА", "БРАЗЕ") == ["yellow"] * 5

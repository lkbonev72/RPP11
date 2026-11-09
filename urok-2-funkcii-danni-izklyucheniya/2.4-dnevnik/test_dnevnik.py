"""Проверки за задача 2.4: модулът dnevnik.py.

Пускане:  python -m pytest urok-2-funkcii-danni-izklyucheniya/2.4-dnevnik -v
"""
import pytest

from dnevnik import (STUDENTS, at_risk, class_ranking, overall_average,
                     subject_average, weakest_subject)

ANI = STUDENTS["Ани"]
VERA = STUDENTS["Вера"]
GEORGI = STUDENTS["Георги"]


# ---------- subject_average ----------

def test_subject_average():
    assert subject_average(ANI, "математика") == pytest.approx(17 / 3)


def test_subject_average_prazen_spisuk():
    assert subject_average(VERA, "история") is None


def test_subject_average_lipsvasht_predmet():
    assert subject_average(ANI, "химия") is None


def test_subject_average_uchenik_bez_otsenki():
    assert subject_average(GEORGI, "математика") is None


# ---------- overall_average ----------

def test_overall_average_e_sredno_na_srednite():
    # (17/3 + 5.5 + 6) / 3, а не средното на всички 6 оценки
    assert overall_average(ANI) == pytest.approx((17 / 3 + 5.5 + 6) / 3)


def test_overall_average_propuska_predmet_bez_otsenki():
    assert overall_average(VERA) == pytest.approx(5.5)


def test_overall_average_bez_otsenki():
    assert overall_average(GEORGI) is None


# ---------- weakest_subject ----------

def test_weakest_subject():
    assert weakest_subject(STUDENTS["Борис"]) == "български"


def test_weakest_subject_ravenstvo_po_azbuchen_red():
    assert weakest_subject({"химия": [4], "биология": [4], "физика": [5]}) == "биология"


def test_weakest_subject_bez_otsenki():
    assert weakest_subject(GEORGI) is None


# ---------- class_ranking ----------

def test_class_ranking_red():
    names = [name for name, _ in class_ranking(STUDENTS)]
    assert names == ["Ани", "Вера", "Борис", "Диана", "Георги"]


def test_class_ranking_bez_otsenki_e_nakraya_s_none():
    assert class_ranking(STUDENTS)[-1] == ("Георги", None)


def test_class_ranking_ravenstvo_po_azbuchen_red():
    students = {"Яна": {"м": [5]}, "Ася": {"м": [5]}, "Иво": {"м": [6]}}
    assert [n for n, _ in class_ranking(students)] == ["Иво", "Ася", "Яна"]


def test_class_ranking_prazen_rechnik():
    assert class_ranking({}) == []


# ---------- at_risk ----------

def test_at_risk():
    assert at_risk(STUDENTS) == ["Борис", "Диана"]


def test_at_risk_drug_prag():
    assert at_risk(STUDENTS, threshold=3.10) == ["Диана"]


def test_at_risk_tochno_na_praga_ne_e_v_risk():
    # Диана е с успех точно 3.00 — „под прага“ означава строго по-малко
    assert at_risk(STUDENTS, threshold=3.0) == []


def test_at_risk_prazen_rechnik():
    assert at_risk({}) == []


# ---------- общо ----------

def test_funktsiite_ne_pechatat(capsys):
    subject_average(ANI, "математика")
    overall_average(ANI)
    weakest_subject(ANI)
    class_ranking(STUDENTS)
    at_risk(STUDENTS)
    assert capsys.readouterr().out == ""

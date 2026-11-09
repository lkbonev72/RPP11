"""Проверки за задача 2.1, стъпка 1: функцията to_int16.

Пускане:  python -m pytest urok-2-funkcii-danni-izklyucheniya/2.1-spasete-ariane -v
"""
import pytest

from ariane import INT16_MAX, INT16_MIN, OverflowAlarm, to_int16


def test_obiknovena_stoynost():
    assert to_int16(28800.0) == 28800


def test_vrashta_cyalo_chislo():
    assert isinstance(to_int16(1440.0), int)


def test_otritsatelna_stoynost():
    assert to_int16(-1200.0) == -1200


def test_gornata_granitsa_se_pobira():
    assert to_int16(float(INT16_MAX)) == INT16_MAX


def test_dolnata_granitsa_se_pobira():
    assert to_int16(float(INT16_MIN)) == INT16_MIN


def test_nad_gornata_granitsa_vdiga_overflowalarm():
    with pytest.raises(OverflowAlarm):
        to_int16(INT16_MAX + 1.0)


def test_pod_dolnata_granitsa_vdiga_overflowalarm():
    with pytest.raises(OverflowAlarm):
        to_int16(INT16_MIN - 1.0)


def test_stoynostta_ot_avariyata_vdiga_overflowalarm():
    with pytest.raises(OverflowAlarm):
        to_int16(36450.0)


def test_izklyuchenieto_nosi_stoynostta():
    with pytest.raises(OverflowAlarm) as info:
        to_int16(45000.0)
    assert info.value.value == 45000.0

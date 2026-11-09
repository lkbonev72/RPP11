"""Проверки за задача 2.2: новите функции в bufet.py.

Пускане:  python -m pytest urok-2-funkcii-danni-izklyucheniya/2.2-bufet -v

Всяка проверка работи с прясно копие на STOCK, затова редът
на проверките няма значение.
"""
import copy

import pytest

import bufet


def nuzhno(name):
    """Връща функцията или класа name от bufet.py или проваля проверката с ясно съобщение."""
    obj = getattr(bufet, name, None)
    if obj is None:
        pytest.fail(f"В bufet.py още няма '{name}'.")
    return obj


@pytest.fixture
def stock():
    return copy.deepcopy(bufet.STOCK)


# ---------- PriceError ----------

def test_priceerror_nasledyava_bufeterror():
    PriceError = nuzhno("PriceError")
    assert issubclass(PriceError, bufet.BufetError)


# ---------- deliver ----------

def test_deliver_uvelichava_nalichnostta(stock):
    deliver = nuzhno("deliver")
    deliver(stock, "кроасан", 6)
    assert stock["кроасан"]["kolichestvo"] == 10


def test_deliver_vrashta_novoto_kolichestvo(stock):
    deliver = nuzhno("deliver")
    assert deliver(stock, "сандвич", 3) == 3


def test_deliver_nov_produkt_s_tsena(stock):
    deliver = nuzhno("deliver")
    deliver(stock, "йогурт", 12, cena=1.60)
    assert stock["йогурт"] == {"cena": 1.60, "kolichestvo": 12}


def test_deliver_nov_produkt_bez_tsena_vdiga_unknownproduct(stock):
    deliver = nuzhno("deliver")
    with pytest.raises(bufet.UnknownProduct):
        deliver(stock, "йогурт", 12)
    assert "йогурт" not in stock


def test_deliver_otritsatelna_tsena_vdiga_priceerror(stock):
    deliver, PriceError = nuzhno("deliver"), nuzhno("PriceError")
    with pytest.raises(PriceError):
        deliver(stock, "йогурт", 12, cena=-1.00)


def test_deliver_nuleva_tsena_vdiga_priceerror(stock):
    deliver, PriceError = nuzhno("deliver"), nuzhno("PriceError")
    with pytest.raises(PriceError):
        deliver(stock, "йогурт", 12, cena=0)


def test_deliver_nevalidno_kolichestvo_vdiga_valueerror(stock):
    deliver = nuzhno("deliver")
    with pytest.raises(ValueError):
        deliver(stock, "банан", 0)


# ---------- apply_discount ----------

def test_apply_discount_za_uchitel():
    apply_discount = nuzhno("apply_discount")
    assert apply_discount(10.00, True) == pytest.approx(9.00)


def test_apply_discount_za_uchenik():
    apply_discount = nuzhno("apply_discount")
    assert apply_discount(10.00, False) == pytest.approx(10.00)


def test_apply_discount_zakruglyava_do_stotinka():
    apply_discount = nuzhno("apply_discount")
    assert apply_discount(6.70, True) == round(6.70 * 0.9, 2)
    assert apply_discount(3.33, True) == 3.0


# ---------- daily_report ----------

def test_daily_report_obshta_stoynost(stock):
    daily_report = nuzhno("daily_report")
    assert daily_report(stock)["obshta_stoynost"] == pytest.approx(44.50)


def test_daily_report_nay_skap_produkt(stock):
    daily_report = nuzhno("daily_report")
    assert daily_report(stock)["nay_skap"] == "сандвич"


def test_daily_report_broy_izcherpani(stock):
    daily_report = nuzhno("daily_report")
    assert daily_report(stock)["izcherpani"] == 1


def test_daily_report_ne_pechata(stock, capsys):
    daily_report = nuzhno("daily_report")
    daily_report(stock)
    assert capsys.readouterr().out == "", "daily_report трябва да връща, а не да печата"


def test_daily_report_prazen_bufet():
    daily_report = nuzhno("daily_report")
    report = daily_report({})
    assert report["obshta_stoynost"] == 0
    assert report["nay_skap"] is None
    assert report["izcherpani"] == 0

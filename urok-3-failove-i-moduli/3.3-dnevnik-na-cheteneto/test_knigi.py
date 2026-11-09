"""Проверки за задача 3.3: дневник на четенето.

Пускане:  python -m pytest urok-3-failove-i-moduli/3.3-dnevnik-na-cheteneto -v
"""
import shutil
from pathlib import Path

import pytest

from knigi import add_book, export_report, load_books, stats

PRIMER = Path(__file__).parent / "knigi.txt"


@pytest.fixture
def fail(tmp_path):
    """Копие на knigi.txt, за да не се променя оригиналът."""
    path = tmp_path / "knigi.txt"
    shutil.copy(PRIMER, path)
    return path


# ---------- load_books ----------

def test_load_books_broy(fail):
    books, skipped = load_books(fail)
    assert len(books) == 8
    assert skipped == 3


def test_load_books_struktura(fail):
    books, _ = load_books(fail)
    assert books[0] == {"zaglavie": "Под игото", "avtor": "Иван Вазов",
                        "godina": 2025, "otsenka": 5}


def test_load_books_zaglavie_sas_zapetaya(tmp_path):
    path = tmp_path / "k.txt"
    path.write_text("Лъвът, вещицата и гардеробът | К. С. Луис | 2026 | 6\n", encoding="utf-8")
    books, skipped = load_books(path)
    assert books[0]["zaglavie"] == "Лъвът, вещицата и гардеробът"
    assert skipped == 0


def test_load_books_lipsvasht_fail(tmp_path):
    assert load_books(tmp_path / "nyama.txt") == ([], 0)


def test_load_books_prazni_redove_ne_sa_povredeni(tmp_path):
    path = tmp_path / "k.txt"
    path.write_text("\nТютюн | Димитър Димов | 2025 | 4\n\n", encoding="utf-8")
    books, skipped = load_books(path)
    assert len(books) == 1
    assert skipped == 0


# ---------- add_book ----------

def test_add_book_dobavya_bez_da_prezapisva(fail):
    add_book(fail, "Дюн", "Франк Хърбърт", 2026, 6)
    books, skipped = load_books(fail)
    assert len(books) == 9
    assert books[-1]["zaglavie"] == "Дюн"


def test_add_book_v_nov_fail(tmp_path):
    path = tmp_path / "nov.txt"
    add_book(path, "Дюн", "Франк Хърбърт", 2026, 6)
    add_book(path, "Тютюн", "Димитър Димов", 2026, 4)
    books, _ = load_books(path)
    assert [b["zaglavie"] for b in books] == ["Дюн", "Тютюн"]


def test_add_book_nevalidna_otsenka(fail):
    predi = fail.read_text(encoding="utf-8")
    with pytest.raises(ValueError):
        add_book(fail, "Дюн", "Франк Хърбърт", 2026, 7)
    assert fail.read_text(encoding="utf-8") == predi


# ---------- stats ----------

def test_stats_sredna_otsenka(fail):
    books, _ = load_books(fail)
    assert stats(books)["sredna_otsenka"] == pytest.approx(42 / 8)


def test_stats_nay_dobra_parvata_s_nay_visoka(fail):
    books, _ = load_books(fail)
    assert stats(books)["nay_dobra"] == "Бай Ганьо"


def test_stats_po_godini(fail):
    books, _ = load_books(fail)
    assert stats(books)["po_godini"] == {2025: 4, 2026: 4}


def test_stats_prazen_spisak():
    result = stats([])
    assert result["sredna_otsenka"] is None
    assert result["nay_dobra"] is None
    assert result["po_godini"] == {}


# ---------- export_report ----------

def test_export_report_e_v_utf8(fail, tmp_path):
    books, _ = load_books(fail)
    otchet = tmp_path / "otchet.txt"
    export_report(otchet, books)
    text = otchet.read_bytes().decode("utf-8")   # гърми, ако не е UTF-8
    for book in books:
        assert book["zaglavie"] in text

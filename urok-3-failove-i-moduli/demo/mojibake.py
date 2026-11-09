"""mojibake.py — една и съща буква, различни байтове.

Програмата записва текст така, както го е правила програма от 90-те
(в cp1251), и после се опитва да го прочете по три различни начина.
"""
from pathlib import Path

TEXT = "Здравей, свят! Тест с кодиране."
FILE = Path(__file__).parent / "test_cp1251.txt"


def write_in_cp1251() -> None:
    """Записваме текста така, както го е правила програма от 90-те."""
    with open(FILE, "w", encoding="cp1251") as f:
        f.write(TEXT)


def read_wrong() -> None:
    """Четем същия файл, все едно е UTF-8."""
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            print("   ", f.read())
    except UnicodeDecodeError as err:
        bad = err.object[err.start]
        print(f"    UnicodeDecodeError: {err.reason}")
        print(f"    Проблемен байт на позиция {err.start}: 0x{bad:02x} ({bad})")


def read_latin1() -> None:
    """Четем като latin-1: не гърми, но дава безсмислица — най-коварният случай."""
    with open(FILE, "r", encoding="latin-1") as f:
        print("   ", f.read())


def read_right() -> None:
    """Четем с кодирането, с което файлът е записан."""
    with open(FILE, "r", encoding="cp1251") as f:
        print("   ", f.read())


def show_bytes() -> None:
    for enc in ("cp1251", "utf-8", "utf-16-le"):
        raw = "Я".encode(enc)
        print(f"    {enc:10s} -> {len(raw)} байта: {raw.hex(' ')}")


if __name__ == "__main__":
    write_in_cp1251()
    print("1) Четене като UTF-8 (грешно):")
    read_wrong()
    print("2) Четене като latin-1 (не гърми, но е безсмислица):")
    read_latin1()
    print("3) Четене с правилното кодиране cp1251:")
    read_right()
    print("4) Буквата 'Я' в различни кодирания:")
    show_bytes()

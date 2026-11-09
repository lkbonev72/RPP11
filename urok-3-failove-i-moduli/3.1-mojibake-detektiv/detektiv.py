"""detektiv.py — в какво кодиране е записан файлът?

Задача 3.1. Четирите файла tekst_a.txt … tekst_d.txt съдържат един
и същ текст, но са записани в различни кодирания.
"""
from pathlib import Path

HERE = Path(__file__).parent
FILES = ["tekst_a.txt", "tekst_b.txt", "tekst_c.txt", "tekst_d.txt"]
ENCODINGS = ["utf-8", "cp1251", "utf-16", "latin-1"]

# Знаци, които почти никога не се срещат в български текст,
# но са типични за mojibake. Допълнете списъка, ако е нужно.
SUSPICIOUS = "ÃÐÑñÿÇäðàâåé"


def preview(path, encoding: str, n: int = 40) -> str:
    """Първите n символа от файла, прочетен с даденото кодиране.

    Ако файлът не може да се прочете с това кодиране,
    UnicodeDecodeError не се прехваща тук — нека реши викащият.
    """
    # СТЪПКА 2
    raise NotImplementedError


def guess_encoding(path):
    """Името на първото кодиране от ENCODINGS, при което текстът
    съдържа български букви и няма знаци от SUSPICIOUS.
    None, ако нито едно не пасва.
    """
    # СТЪПКА 3
    raise NotImplementedError


def main() -> None:
    for name in FILES:
        print(f"\n=== {name} ===")
        for enc in ENCODINGS:
            # СТЪПКА 2: отпечатайте preview(...) или кратко съобщение,
            # ако кодирането не става.
            pass
        # СТЪПКА 3: отпечатайте догадката guess_encoding(...)


if __name__ == "__main__":
    main()

# СТЪПКА 4: кога методът ви би сгрешил? Отговорете тук в коментар.
#

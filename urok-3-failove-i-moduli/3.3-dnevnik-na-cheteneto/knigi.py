"""knigi.py — дневник на прочетените книги в текстов файл.

Задача 3.3. Един ред във файла е една книга:

    заглавие | автор | година на прочитане | оценка от 1 до 6

Правила: файлът се отваря само с with и само с явно кодиране;
повреден ред не спира програмата.
"""
from pathlib import Path

HERE = Path(__file__).parent
KNIGI = HERE / "knigi.txt"


def add_book(path, title: str, author: str, year: int, rating: int) -> None:
    """Добавя ред в края на файла, без да презаписва старите.

    При оценка извън 1..6 вдига ValueError и не пише нищо.
    """
    raise NotImplementedError


def load_books(path) -> tuple:
    """Чете файла. Връща (книги, брой_пропуснати_редове).

    Всяка книга е речник с ключове "zaglavie", "avtor",
    "godina" (int) и "otsenka" (int).
    Пропуска повредените редове: с друг брой полета, с година
    или оценка, която не е число, или с оценка извън 1..6.
    Ако файлът липсва, дневникът е празен: връща ([], 0).
    """
    raise NotImplementedError


def stats(books: list) -> dict:
    """Връща речник с ключове:

    "sredna_otsenka" — средната оценка (None при празен списък),
    "nay_dobra"      — заглавието с най-висока оценка
                       (при равенство — първото във файла; None при празен списък),
    "po_godini"      — речник {година: брой книги}.
    """
    raise NotImplementedError


def export_report(path, books: list) -> None:
    """Записва подреден текстов отчет в UTF-8."""
    raise NotImplementedError


if __name__ == "__main__":
    books, skipped = load_books(KNIGI)
    print(f"Заредени {len(books)} книги, пропуснати {skipped} повредени реда.")

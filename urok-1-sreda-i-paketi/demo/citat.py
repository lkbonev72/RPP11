"""citat.py — цитат на деня.

Програмата работи и без инсталиран пакет rich, но тогава сама казва
какво липсва. Така искаме да се държат всички наши проекти:
липсващата зависимост е разбираемо съобщение, а не загадъчна грешка.
"""
import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

QUOTES = [
    ("Първо накарай кода да работи, после го направи бърз.", "Кент Бек"),
    ("Програмите трябва да се пишат, за да ги четат хора.", "Харолд Абелсън"),
    ("Простотата е предпоставка за надеждност.", "Едсхер Дейкстра"),
]


def quote_of_the_day(day: datetime.date) -> tuple:
    """Един и същ цитат за целия ден, различен за всеки ден."""
    return QUOTES[day.toordinal() % len(QUOTES)]


def main() -> None:
    today = datetime.date.today()
    text, author = quote_of_the_day(today)
    if HAS_RICH:
        Console().print(Panel(f"[italic]{text}[/italic]\n\n[bold]— {author}[/bold]",
                              title=f"Цитат за {today:%d.%m.%Y}", border_style="cyan"))
    else:
        print("Пакетът 'rich' не е инсталиран в тази среда.")
        print("Направи:  python -m pip install -r requirements.txt")
        print(f"\n{text}\n— {author}")


if __name__ == "__main__":
    main()

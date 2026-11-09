"""main.py — <име на приложението>.

<Какво прави програмата — едно изречение.>
"""
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def main() -> None:
    """Главният цикъл на програмата: само вход и изход."""
    print("<ИМЕ НА ПРИЛОЖЕНИЕТО>")
    # Тук: зареждане на данните, меню / игрови цикъл, запис при изход.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nДовиждане!")

"""main.py — само вход и изход. Нищо друго."""
from pathlib import Path

from analiz import frequency, statistics, to_words, top_n
from chetene import read_text

# Пътят се смята спрямо папката на main.py, затова програмата
# работи, откъдето и да я стартирате.
DATA = Path(__file__).parent / "data" / "tekst.txt"


def main() -> None:
    text = read_text(DATA)
    print("СТАТИСТИКА")
    for key, value in statistics(text).items():
        print(f"  {key:20s}: {value}")
    print("\nНАЙ-ЧЕСТИ ДУМИ")
    for word, count in top_n(frequency(to_words(text)), 8):
        print(f"  {word:15s} {count:2d} {'#' * count}")


if __name__ == "__main__":
    main()

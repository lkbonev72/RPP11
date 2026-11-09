"""analiz.py — чистата логика. Не знае нищо за файлове и печатане."""

PUNCTUATION = ".,!?;:\"'„“”()-–—…«»\n\t"


def to_words(text: str) -> list:
    """Разделя текста на думи с малки букви, без пунктуация."""
    cleaned = text
    for ch in PUNCTUATION:
        cleaned = cleaned.replace(ch, " ")
    return [w for w in cleaned.lower().split() if w]


def frequency(words: list) -> dict:
    """Колко пъти се среща всяка дума."""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_n(counts: dict, n: int = 10) -> list:
    """Най-честите n думи; при равен брой — по азбучен ред."""
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]


def statistics(text: str) -> dict:
    """Основни числа за текста."""
    words = to_words(text)
    return {
        "символи": len(text),
        "думи": len(words),
        "различни думи": len(frequency(words)),
        "най-дълга дума": max(words, key=len) if words else "",
    }


if __name__ == "__main__":
    # Проверките работят, без на диска да има какъвто и да е файл.
    assert to_words("Чете, чете — и пак чете!") == ["чете", "чете", "и", "пак", "чете"]
    assert frequency(["а", "б", "а"]) == {"а": 2, "б": 1}
    assert top_n({"б": 2, "а": 2, "в": 5}, 2) == [("в", 5), ("а", 2)]
    assert statistics("")["думи"] == 0
    assert statistics("Едно две две")["различни думи"] == 2
    print("analiz.py: всички проверки минаха.")

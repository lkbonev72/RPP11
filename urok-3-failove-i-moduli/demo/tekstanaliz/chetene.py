"""chetene.py — всичко, свързано с файлове."""


def read_text(path, encoding: str = "utf-8") -> str:
    """Чете текстов файл. Ако кодирането е грешно, казва го ясно."""
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise SystemExit(f"Няма такъв файл: {path}")
    except UnicodeDecodeError:
        raise SystemExit(f"Файлът {path} не е в {encoding}. Опитай cp1251.")


def save_report(path, lines: list) -> None:
    """Записва редовете във файл в UTF-8, по един на ред."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

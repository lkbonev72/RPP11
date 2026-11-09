"""load_config.py — чете настройки от вида ключ=число.

Задача 2.3: в тази функция има четири проблема. Намерете ги,
опишете ги в otgovori.md и напишете поправена версия тук.
"""
from pathlib import Path

HERE = Path(__file__).parent  # папката на този файл, откъдето и да го стартирате


def load_config(path):
    try:
        f = open(path)
        data = {}
        for line in f:
            key, value = line.split('=')
            data[key] = int(value)
        return data
    except:
        return {}


if __name__ == "__main__":
    for name in ("nastroyki.txt", "nastroyki_povredeni.txt", "nyama_takav_fail.txt"):
        print(f"{name:28s} -> {load_config(HERE / name)}")

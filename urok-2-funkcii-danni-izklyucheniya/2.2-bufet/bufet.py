"""bufet.py — училищният бюфет: речници, функции и йерархия от изключения.

Задача 2.2: разширете модула с функциите от README.md на урока.
"""

STOCK = {
    "банан":   {"cena": 1.20, "kolichestvo": 10},
    "кроасан": {"cena": 2.50, "kolichestvo": 4},
    "вода":    {"cena": 0.90, "kolichestvo": 25},
    "сандвич": {"cena": 3.80, "kolichestvo": 0},
}


class BufetError(Exception):
    """Базово изключение на бюфета — всички останали наследяват него."""


class UnknownProduct(BufetError):
    pass


class NotEnoughStock(BufetError):
    def __init__(self, name, wanted, available):
        super().__init__(f"Искаш {wanted} бр. '{name}', а има само {available} бр.")
        self.name, self.wanted, self.available = name, wanted, available


def sell(stock: dict, name: str, quantity: int) -> float:
    """Продава quantity броя от name. Връща сумата."""
    if name not in stock:
        raise UnknownProduct(f"Няма продукт '{name}' в бюфета")
    if quantity <= 0:
        raise ValueError("Количеството трябва да е положително цяло число")
    item = stock[name]
    if item["kolichestvo"] < quantity:
        raise NotEnoughStock(name, quantity, item["kolichestvo"])
    item["kolichestvo"] -= quantity
    return round(item["cena"] * quantity, 2)


def receipt(stock: dict, order: list) -> tuple:
    """Обработва поръчка. Връща (сума, редове на бележката, проблеми)."""
    total, lines, problems = 0.0, [], []
    for name, quantity in order:
        try:
            price = sell(stock, name, quantity)
        except BufetError as err:
            problems.append(str(err))
        except ValueError as err:
            problems.append(f"Невалидно количество за '{name}': {err}")
        else:
            total += price
            lines.append(f"{name:10s} x{quantity:2d} = {price:6.2f} лв.")
    return round(total, 2), lines, problems


def low_stock(stock: dict, threshold: int = 5) -> list:
    """Имена на продуктите, които трябва да се доставят."""
    return sorted(name for name, item in stock.items()
                  if item["kolichestvo"] <= threshold)


# ---------------------------------------------------------------
# ЗАДАЧА 2.2: добавете тук PriceError, deliver, apply_discount
# и daily_report. Условието е в README.md на урока.
# ---------------------------------------------------------------


if __name__ == "__main__":
    order = [("банан", 2), ("кроасан", 1), ("сандвич", 1),
             ("пица", 1), ("вода", -3), ("вода", 2)]
    total, lines, problems = receipt(STOCK, order)

    print("КАСОВА БЕЛЕЖКА")
    for line in lines:
        print("  " + line)
    print(f"  ОБЩО: {total:.2f} лв.")

    if problems:
        print("\nНЕИЗПЪЛНЕНИ ПОЗИЦИИ:")
        for problem in problems:
            print(f"  - {problem}")

    print(f"\nЗА ДОСТАВКА: {', '.join(low_stock(STOCK))}")

    # ЗАДАЧА 2.2: добавете тук поне 6 сценария с новите функции,
    # включително три, които предизвикват различни изключения.

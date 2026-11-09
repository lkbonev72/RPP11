"""debug_demo.py — logging и assert в действие.

Сменете level=logging.DEBUG на level=logging.INFO и стартирайте отново:
едно число превключва целия изход между „подробно“ и „само важното“,
без да се пипа нито един ред в тялото на функциите.
"""
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-8s %(funcName)-14s %(message)s",
)
log = logging.getLogger(__name__)


def apply_discount(price: float, percent: float) -> float:
    """Намалява цената с percent процента."""
    log.debug("вход: price=%.2f percent=%.1f", price, percent)
    assert 0 <= percent <= 100, f"Процентът трябва да е 0–100, а е {percent}"
    discount = price * percent / 100
    result = round(price - discount, 2)
    log.debug("отстъпка=%.2f -> резултат=%.2f", discount, result)
    if result < 0:
        log.error("Отрицателна цена! Нещо е сбъркано.")
    return result


def basket_total(items: list) -> float:
    """Сума на кошницата; артикулите с невъзможна отстъпка се пропускат."""
    total = 0.0
    for name, price, percent in items:
        # breakpoint()   # махнете # и стартирайте: n, p name, p total, c
        try:
            final = apply_discount(price, percent)
        except AssertionError as err:
            log.warning("Пропускам '%s': %s", name, err)
            continue
        log.info("%-12s %6.2f -> %6.2f", name, price, final)
        total += final
    return round(total, 2)


if __name__ == "__main__":
    basket = [
        ("раница", 59.90, 25),
        ("калкулатор", 34.00, 150),
        ("тетрадка", 4.20, 20),
    ]
    print(f"ОБЩО ЗА ПЛАЩАНЕ: {basket_total(basket):.2f} лв.")

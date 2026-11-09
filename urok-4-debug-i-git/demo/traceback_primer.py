"""traceback_primer.py — как се чете traceback.

Стартирайте и прочетете грешката ОТДОЛУ НАГОРЕ.
Къде гръмна програмата? А къде е причината?
"""

CENI = {"банан": 1.20, "кроасан": 2.50, "вода": 0.90}


def cena(produkt):
    return CENI[produkt]


def suma(porachka):
    total = 0
    for produkt, broy in porachka:
        total += cena(produkt) * broy
    return total


def pechatay_smetka(porachka):
    print(f"Сума: {suma(porachka):.2f} лв.")


if __name__ == "__main__":
    pechatay_smetka([("банан", 2), ("круасан", 1)])

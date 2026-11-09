"""vsichko.py — анализ на продажбите в училищния бюфет за една седмица.

Програмата работи, но в нея всичко е смесено: четене на файла,
изчисления и печатане са в едни и същи функции, данните са в
глобални променливи, а основната програма е разпиляна на нивото
на модула.

Задача 3.2: разделете я на chetene.py, analiz.py и main.py.
След разделянето python main.py трябва да дава ТОЧНО същия изход.
"""
from pathlib import Path

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "prodazhbi.txt"
REPORT_FILE = HERE / "otchet.txt"

DAYS = ["понеделник", "вторник", "сряда", "четвъртък", "петък", "събота", "неделя"]

prodazhbi = []
propusnati = 0


def zaredi():
    global propusnati
    f = open(DATA_FILE, encoding="utf-8")
    for nomer, red in enumerate(f, start=1):
        red = red.strip()
        if not red or red.startswith("#"):
            continue
        chasti = [c.strip() for c in red.split("|")]
        if len(chasti) != 4:
            print(f"  Ред {nomer}: очаквах 4 полета, а са {len(chasti)} — пропускам")
            propusnati += 1
            continue
        data, produkt, broy, cena = chasti
        try:
            broy = int(broy)
            cena = float(cena)
        except ValueError:
            print(f"  Ред {nomer}: '{chasti[2]}' или '{chasti[3]}' не е число — пропускам")
            propusnati += 1
            continue
        prodazhbi.append({"data": data, "produkt": produkt, "broy": broy, "cena": cena})
    f.close()
    print(f"Заредени {len(prodazhbi)} продажби, пропуснати {propusnati} реда.")


def oborot_po_produkti():
    rezultat = {}
    for p in prodazhbi:
        suma = p["broy"] * p["cena"]
        if p["produkt"] in rezultat:
            rezultat[p["produkt"]] = rezultat[p["produkt"]] + suma
        else:
            rezultat[p["produkt"]] = suma
    print("\nОБОРОТ ПО ПРОДУКТИ")
    for produkt, suma in sorted(rezultat.items(), key=lambda x: -x[1]):
        print(f"  {produkt:10s} {suma:8.2f} лв.")
    return rezultat


def oborot_po_dni():
    import datetime
    rezultat = {}
    for p in prodazhbi:
        rezultat[p["data"]] = rezultat.get(p["data"], 0) + p["broy"] * p["cena"]
    print("\nОБОРОТ ПО ДНИ")
    nay_dobur = None
    for data in sorted(rezultat):
        den = DAYS[datetime.date.fromisoformat(data).weekday()]
        print(f"  {data}  {den:11s}{rezultat[data]:8.2f} лв.")
        if nay_dobur is None or rezultat[data] > rezultat[nay_dobur]:
            nay_dobur = data
    print(f"  Най-добър ден: {nay_dobur}")
    return rezultat


def nay_prodavan():
    broyki = {}
    for p in prodazhbi:
        broyki[p["produkt"]] = broyki.get(p["produkt"], 0) + p["broy"]
    nay = ""
    for produkt in broyki:
        if nay == "" or broyki[produkt] > broyki[nay]:
            nay = produkt
    print(f"\nНАЙ-ПРОДАВАН ПРОДУКТ: {nay} ({broyki[nay]} бр.)")
    sredno = sum(broyki.values()) / len(broyki)
    print(f"Средно продадени бройки на продукт: {sredno:.1f}")


def zapishi_otchet(po_produkti, po_dni):
    obshto = 0
    for p in prodazhbi:
        obshto = obshto + p["broy"] * p["cena"]
    print(f"\nОБЩ ОБОРОТ: {obshto:.2f} лв.")
    f = open(REPORT_FILE, "w", encoding="utf-8")
    f.write("ОТЧЕТ ЗА СЕДМИЦАТА\n")
    f.write(f"Общ оборот: {obshto:.2f} лв.\n\n")
    f.write("По продукти:\n")
    for produkt, suma in sorted(po_produkti.items(), key=lambda x: -x[1]):
        f.write(f"  {produkt}: {suma:.2f} лв.\n")
    f.write("\nПо дни:\n")
    for data in sorted(po_dni):
        f.write(f"  {data}: {po_dni[data]:.2f} лв.\n")
    f.close()
    print(f"Отчетът е записан в {REPORT_FILE.name}")


print("АНАЛИЗ НА ПРОДАЖБИТЕ В БЮФЕТА")
zaredi()
po_produkti = oborot_po_produkti()
po_dni = oborot_po_dni()
nay_prodavan()
zapishi_otchet(po_produkti, po_dni)

STUDENTS = {
    "Ани": [6, 5, 6, 4],
    "Борис": [3, 4, 3],
    "Валентин": [5, 6, 6, 5],
    "Вера": [5, 5, 6, 6, 5],
    "Георги": [],
    "Диана": [6, 6, 6],
}


def average(grades):
    total = 0
    for g in grades:
        total += g
    return total / len(grades)


def is_excellent(avg):
    return avg > 5.50


def ranking(students):
    result = []
    for name in students:
        result.append((name, average(students[name])))
    result.sort(key=lambda pair: pair[1])
    return result


def print_report(students):
    print("КЛАСАЦИЯ")
    position = 0
    for name, avg in ranking(students):
        position += 1
        mark = " *" if is_excellent(avg) else ""
        print(f"{position}. {name:10s} {avg:.2f}{mark}")
    all_grades = []
    for name in students:
        all_grades = students[name]
    print(f"Среден успех на класа: {average(all_grades):.2f}")
    print(f"Брой отличници: {len(students) - position}")


if __name__ == "__main__":
    print_report(STUDENTS)
    print(f"Най-добър ученик: {ranking(STUDENTS)[0][0]}")

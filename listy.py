l1 = 0
def list1() -> object:
    list_1 = []
    l1 = int(input("Podaj liczbę elementów do posortowania\n"))

    for i in range(0, l1):
        elements_1 = [int(input("Wprowadź liczby do sortowania w dowolnej kolejności\n"))]
        list_1.append(elements_1)

    return list_1


def list2():
    list_2 = []

    for j in range(0, l1):
        elements_2 = [int(input("Wprowadź te same liczby, w kolejności od najmniejszej do największej\n"))]
        list_2.append(elements_2)
    return list_2
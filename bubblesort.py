class Bubble_sort():
        @staticmethod
        def sortowanie(lista):
            x = len(lista)
            while x > 1:
                zamiania = False
                for i in range(0, x - 1):
                        if lista[i] > lista[i + 1]:
                            lista[i], lista[i + 1] = lista[i + 1], lista[i]
                            zamiana = True
                x -= 1
                print(lista)
                if zamiana == False: break
            return lista

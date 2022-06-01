import bubblesorttest
import bubblesort
import unittest
import os
import listy


print("*******************************************************************")
print("*************************** MENU GLÓWNE ***************************")
print("*******************************************************************")
print("**  Wybierz z menu wpisując odpowiednio   *************************")
print("**  1 - test nr 1 --> przypadek trywialny  ************************")
print("**  2 - test nr 2 --> przypadek skomplikowany  ********************")
print("*******************************************************************")
def menu():
    x = input("Wprowadź liczbę\n")

    if x == "1":
        print("Wybrano test nr 1 --> przypadek trywialny")
        bubblesorttest.sortingtest.test_2()
    elif x == "2":
        print("Wybrano test nr 1 --> przypadek skomplikowany")


menu()
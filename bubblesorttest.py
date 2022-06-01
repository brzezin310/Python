import unittest
import listy
from bubblesort import Bubble_sort


class sortingtest(unittest.TestCase):


    def setUp(self):
        pass

    # def test_1(self):   #test pistej listy danych do sortowania
    #   self.assertEqual([],[])

    def __init__(self): # test zadanych liczb do posortowania
        a = listy.list1()
        b = listy.list2()
        self.assertIs(sorted(a), Bubble_sort.sortowanie(b))

    # def test_3(self):  #test liczb z duplikatami
    #   self.assertEqual(sorted([1,1,4,5,6,19,19]),Bubble_sort.sortowanie([4,1,5,1,6,19,19]))

    # def test_4(self): #test sortowania znaków
    #   self.assertEqual(sorted(['a','z','c']),Bubble_sort.sortowanie(['a','c','z']))


if __name__ == '__main__':
    unittest.main()

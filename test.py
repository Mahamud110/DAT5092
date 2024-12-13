import unittest


def add(x,y):
    return x + y

class TestAdd(unittest.TestCase):

    def test_add(self):
        result = add(20,1)
        self.assertEqual(result,15)

if __name__ == '__main__':
    unittest.main()


def multiply(a,b):
    return a*b

class TestMultiply(unittest.TestCase):
   
    def test_multiply(self):
        res = multiply(10,5)
        self.assertEqual(res,50)

if __name__ == '__main__':
    unittest.main()


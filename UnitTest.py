from GOST2814 import GOST2814789MAC
from MD5_HMAC import Fork
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        self.gost = GOST2814789MAC()

    def test_gost(self):
        imitovstavka = "11100001000111101001011100010011"
        with open('TextForTest.txt', 'r') as f:
            text = f.read()
        self.gost.fill_block(text)
        otvet = self.gost.step_mac()
        self.assertEqual(imitovstavka, otvet)

    def test_MD5_HMAC(self):
        expected = "a4c5c7fc432a60ad064ff2f3ac05aba5"
        actual = Fork()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

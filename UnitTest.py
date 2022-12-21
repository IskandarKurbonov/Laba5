from GOST2814 import GOST2814789MAC
from MD5_HMAC import Fork
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        self.gost = GOST2814789MAC()

    def test_gost(self):
        imitovstavka = "10110110101010111110011111100110"
        with open('TextForTest.txt', 'r') as f:
            text = f.read()
        self.gost.fill_block(text)
        otvet = self.gost.step_mac()
        self.assertEqual(imitovstavka, otvet)

    def test_MD5_HMAC(self):
        expected = "3ae70a0f6711cd0af3d616e28fe767a8"
        actual = Fork()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

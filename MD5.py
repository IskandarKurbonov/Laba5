from math import sin
import codecs


class MD5():
    def __init__(self):
        self._word_array = []
        self._r = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                   5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                   4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                   6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
        self._h = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
        self._k = [int((1 << 32) * abs(sin(i))) for i in range(1, 65)]

    def f(self, x, y, z):
        return (x & y) | ((~x) & z)

    def g(self, x, y, z):
        return (x & z) | ((~z) & y)

    def h(self, x, y, z):
        return x ^ y ^ z

    def i(self, x, y, z):
        return y ^ ((~z) | x)

    def xx(self, func, a, b, c, d, xk, s, ti):
        temp = (a + func(b, c, d) + xk + ti) & 0xffffffff
        temp = (temp << s | temp >> (32 - s)) & 0xffffffff
        return (b + temp) & 0xffffffff

    def do_hash(self, in_str):
        len_str = len(in_str)
        result = 0

        for i in range(0, len_str - 3, 4):
            self._word_array.append(int(ord(in_str[i])) |
                                    (int(ord(in_str[i + 1]))) << 8 | (int(ord(in_str[i + 2]))) << 16 | \
                                    (int(ord(in_str[i + 3]))) << 24)
        if len_str % 4 == 0:
            result = 0x080
        elif len_str % 4 == 1:
            result = int(ord(in_str[len_str - 1])) | 0x008000
        elif len_str % 4 == 2:
            result = int(ord(in_str[len_str - 2])) | \
                     int(ord(in_str[len_str - 1])) << 8 | 0x0800000
        elif len_str % 4 == 3:
            result = int(ord(in_str[len_str - 3])) | \
                     int(ord(in_str[len_str - 2])) << 8 | \
                     int(ord(in_str[len_str - 1])) << 16 | 0x80000000
        self._word_array.append(result)
        while len(self._word_array) % 16 != 14:
            self._word_array.append(int(0))
        self._word_array.append(int(len_str << 3) & 0xffffffff)
        self._word_array.append(int(len_str) >> 29)
        w = []
        for j in range(0, len(self._word_array), 16):
            w = self._word_array[j:j + 16]
            aa, bb, cc, dd = self._h[0], self._h[1], self._h[2], self._h[3]
            digit_1 = [(0, 15), (1, 14), (2, 13), (3, 12), (4, 11), (5, 10), (6, 9),
                       (7, 8), (8, 7), (9, 6), (10, 5), (11, 4), (12, 3), (13, 2), (14, 1), (15, 0)]
            digit_2 = [(0, 15, 1), (1, 14, 6), (2, 13, 11), (3, 12, 0), (4, 11, 5),
                       (5, 10, 10), (6, 9, 15), (7, 8, 4), (8, 7, 9), (9, 6, 14), (10, 5, 3),
                       (11, 4, 8), (12, 3, 13), (13, 2, 2), (14, 1, 7), (15, 0, 12)]
            digit_3 = [(0, 15, 5), (1, 14, 8), (2, 13, 11), (3, 12, 14), (4, 11, 1),
                       (5, 10, 4), (6, 9, 7), (7, 8, 10), (8, 7, 13), (9, 6, 0), (10, 5, 3),
                       (11, 4, 6), (12, 3, 9), (13, 2, 12), (14, 1, 15), (15, 0, 2)]
            digit_4 = [(0, 15, 0), (1, 14, 7), (2, 13, 14), (3, 12, 5), (4, 11, 12),
                       (5, 10, 3), (6, 9, 10), (7, 8, 1), (8, 7, 8), (9, 6, 15), (10, 5, 6),
                       (11, 4, 13), (12, 3, 4), (13, 2, 11), (14, 1, 2), (15, 0, 9)]
            for j, k in digit_1:
                self._h[(k + 1) % 4] = self.xx(self.f, self._h[(k + 1) % 4],
                                               self._h[(k + 2) % 4], self._h[(k + 3) % 4], self._h[(k + 4) % 4], w[j],
                                               self._r[j], self._k[j])
            for j, k, m in digit_2:
                self._h[(k + 1) % 4] = self.xx(self.g, self._h[(k + 1) % 4],
                                               self._h[(k + 2) % 4], self._h[(k + 3) % 4], self._h[(k + 4) % 4], w[m],
                                               self._r[j + 16], self._k[j + 16])
            for j, k, m in digit_3:
                self._h[(k + 1) % 4] = self.xx(self.h, self._h[(k + 1) % 4],
                                               self._h[(k + 2) % 4], self._h[(k + 3) % 4], self._h[(k + 4) % 4], w[m],
                                               self._r[j + 32], self._k[j + 32])
            for j, k, m in digit_4:
                self._h[(k + 1) % 4] = self.xx(self.i, self._h[(k + 1) % 4], self._h[(k + 2) % 4],
                                               self._h[(k + 3) % 4], self._h[(k + 4) % 4], w[m],
                                               self._r[j + 48], self._k[j + 48])
            self._h[0] = (self._h[0] + aa) & 0xffffffff
            self._h[1] = (self._h[1] + bb) & 0xffffffff
            self._h[2] = (self._h[2] + cc) & 0xffffffff
            self._h[3] = (self._h[3] + dd) & 0xffffffff

    def hex_digest(self):
        result = ''
        for item in self._h:
            for j in range(7, -1, -2):
                result += str(hex(item)[2:10][j - 1]) + str(hex(item)[2:10][j])
        return result

    def digest(self):
        result = []
        for item in self._h:
            while item:
                result.append(chr(item & 0xff))
                item >>= 8
            result.reverse()
        return ''.join(result)

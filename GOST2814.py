class GOST2814789MAC():
    def __init__(self):
        self._S_block = [[4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
                         [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
                         [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
                         [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
                         [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
                         [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
                         [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
                         [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]]

        self._key = [0x10cbc8cd, 0x2fc0cfc5, 0x34c0ccc1, 0x92cec2c8,
                     0x81ccd8c3, 0x705dcdc8, 0x64c8d8c2, 0x5acecbdf]

    def fill_block(self, in_str):
        self._bin_list = []
        count = 0
        tmp_str = ''
        for i in range(len(in_str)):
            tmp_str += (''.join(map(lambda x: '{0:0>{1}}'.format(bin(ord(x))[2:], 16), in_str[i])))
            count += 1
            if count % 4 == 0:
                self._bin_list.append(tmp_str)
                tmp_str = ''
        while len(tmp_str) != 64:
            tmp_str += '0'
        self._bin_list.append(tmp_str)

    def step_main(self, N, X):
        N1 = int(N[:32], 2)
        N2 = int(N[32:], 2)
        summ = (N1 + X) % (1 << 32)
        S1 = 0
        for j in range(8):
            S = self._S_block[j][(summ >> (28 - j * 4)) & 0xf]
            S1 |= S << (28 - j * 4)
        S1 = ((S1 << 11) | (S1 >> 32 - 11)) & 0xffffffff
        S1 = S1 ^ N2
        N2 = N1
        N1 = S1
        return (bin((N1 << 32) | N2)[2:]).zfill(64)

    def step_mac(self):
        mod_list = '0' * 64
        tmp_str = ''
        for item in self._bin_list:
            for j in range(64):
                tmp_str += str(int(item[j], 2) ^ int(mod_list[j], 2))
            item = tmp_str
            tmp_str = ''
            for k in range(2):
                for i in range(8):
                    item = self.step_main(item, self._key[i])
            mod_list = item[32:] + item[:32]
        return mod_list[:32]


if __name__ == '__main__':
    gost = GOST2814789MAC()
    with open('TextForTest.txt', 'r') as f:
        text = f.read()
    gost.fill_block(text)
    print('Имитовставка = '+gost.step_mac())

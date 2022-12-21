from MD5 import MD5


def Fork():
    with open('TextForTest.txt', 'r') as f:
        text = f.read()
    MESSAGE = text
    KEY = "key"
    trans_5C = "".join ([chr (x ^ 0x5C) for x in range(256)])
    trans_36 = "".join ([chr (x ^ 0x36) for x in range(256)])
    outer = MD5()
    inner = MD5()
    KEY = KEY + chr(0) * (64 - len(KEY))
    inner.do_hash(KEY.translate(trans_36)+MESSAGE)
    outer.do_hash(KEY.translate(trans_5C)+inner.digest())
    result = outer.hex_digest()
    print(result)
    return result
Fork()

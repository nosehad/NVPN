def short_str1(target_string, amount: int = 1):
    result = str()
    for integer in range(len(target_string) - amount):
        result += target_string[integer]
    return result


def short_str2(target_string):
    result = str()
    for integer in range(len(target_string) - 1, 0, -1):
        result = target_string[integer] + result
    return result


def cap_int1(target_int: int, lenght: int = 63):
    binary = [bin(target_int), 0]
    pref = True if binary[0][0] == '-' else False
    if pref: binary[0] = short_str2(binary[0])
    if len(binary[0]) - 2 <= lenght:
        return target_int
    for integer in range((len(binary[0]) - 2) - lenght):
        binary[1] += 1
        pref = False if pref else True
    binary[0] = short_str1(binary[0], binary[1])
    res = ('-' if pref else '') + binary[0]
    return int(res, 2)


class Random:
    def __init__(self, seed: int = -1):
        if seed == -1:
            self.current = self.hardwarebasedrn()
        else:
            self.current: int = seed
        try:
            for integer in range(64):
                self.current / 2
                self.current = self.current * 3 + 1
        except OverflowError:
            self.current = cap_int1(self.current, 63)

    @staticmethod
    def hardwarebasedrn():
        import time
        _t = []
        res = 1

        for integer in range(5):
            start = time.time()
            for integer2 in range(100000):
                _t.append(integer2)
                _t.remove(integer2)
            end = time.time()
            _t = str(end - start)
            while len(_t) > 5:
                _t = short_str2(_t)
            _t = int(_t)
            res *= _t
            _t = []

        return res

    def newbool(self):
        try:
            var = self.current / 2
            self.current = self.current * 3 + 1
        except OverflowError:
            self.current = cap_int1(self.current, 31) # 31 for higher security, since 63 will only produce 588 random
            # numbers
        self.current = cap_int1(self.current)
        return self.current % 2 == 0

    def newselection(self, array):
        return array[self.newboundedint(0, len(array) - 1)]

    def newstring(self, lenght, charset: str = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890'):
        res: str = str()
        for integer in range(lenght):
            res += self.newselection(charset)
        return res

    def newrboundedint(self, lenght: int):
        res: int = 0
        _t: int = 1
        for integer in range(lenght):
            res = res + (1 if self.newbool() else 0) * _t
            _t = _t * 2

        return res

    def newboundedint(self, a: int, b: int):
        if a >= b:
            return a
        c = b - a
        r = self.newrboundedint(len(bin(c)) - 2)
        while not r <= c:
            r = self.newrboundedint(len(bin(c)) - 2)

        return a + r

    def newint(self, raw: bool = False):
        try:
            for integer in range(1):
                self.current / 2
                self.current = self.current * 3 + 1
        except OverflowError:
            self.current = cap_int1(self.current, 31) # 31 for higher security, since 63 will only produce 588 random
            # numbers
            return self.current

        return self.current if raw else cap_int1(self.current)

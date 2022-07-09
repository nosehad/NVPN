from com.nosehad.python.random_c import *


class Hash:
    @staticmethod
    def str_to_int(target_string: str):
        result: int = 0
        _t: int = 1
        for char in target_string:
            for bit in bin(ord(char))[2:]:
                result = result + (1 if bit else 0) * _t
            _t *= 2
        return result

    def __init__(self, target_string: str, lenght: int = 2048, seed: str = 'default'):
        rand1 = Random(self.str_to_int(seed))
        rand2_s: int = 0
        for _ in target_string:
            rand2_s += rand1.newint()
        rand2 = Random(rand2_s)
        self.hashed = rand2.newstring(lenght, "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"
                                              "&#-_")

    def get_hash(self):
        return self.hashed

from com.nosehad.python.random_c import Random
import com.nosehad.python.url as urlib


class UrlDEC:
    def __init__(self, seed):
        self.translation = [['a', 0], ['b', 0], ['c', 0], ['d', 0], ['e', 0], ['f', 0], ['g', 0],
                            ['h', 0], ['i', 0], ['j', 0], ['k', 0], ['l', 0], ['m', 0], ['n', 0],
                            ['o', 0], ['p', 0], ['q', 0], ['r', 0], ['s', 0], ['t', 0], ['u', 0],
                            ['v', 0], ['w', 0], ['x', 0], ['y', 0], ['z', 0], ['A', 0], ['B', 0],
                            ['C', 0], ['D', 0], ['E', 0], ['F', 0], ['G', 0], ['H', 0], ['I', 0],
                            ['J', 0], ['K', 0], ['L', 0], ['M', 0], ['N', 0], ['O', 0], ['P', 0],
                            ['Q', 0], ['R', 0], ['S', 0], ['T', 0], ['U', 0], ['V', 0], ['W', 0],
                            ['X', 0], ['Y', 0], ['Z', 0], [':', 0], ['/', 0], ['=', 0], ['?', 0],
                            ['.', 0], ['&', 0], ['%', 0], ['1', 0], ['2', 0], ['3', 0], ['4', 0],
                            ['5', 0], ['6', 0], ['7', 0], ['8', 0], ['9', 0], ['0', 0], ['-', 0],
                            ['_', 0], ['+', 0]]
        random = Random(seed)
        for char in self.translation:
            string = random.newstring(lenght=2)
            while self.match(string=string):
                string = random.newstring(lenght=2)
            char[1] = string

    def decrypt(self, turl):
        res = str()
        extension = urlib.get_extension(turl)
        url = turl.replace(extension, '')
        integer = 0
        while integer < len(url):
            found = False
            for char2 in self.translation:
                if url[integer] + url[integer + 1] == char2[1]:
                    res += char2[0]
                    found = True
                    break
            if not found:
                temp = str()
                for integer in range(len(turl) - 1, integer, -1):
                    temp = turl[integer] + temp
                return res + extension + temp
            integer += 2
        return res + extension

    def match(self, string):
        for char in self.translation:
            if char[1] == string:
                return True
        return False

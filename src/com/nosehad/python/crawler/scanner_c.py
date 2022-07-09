from com.nosehad.python.url_encrypter_c import UrlENC

points = [['"', '"'], ['\'', '\''], ['(', ')'], ['=', '> ']]  # [<start>, <end>]


class Scanner:

    def __init__(self, string: str, uri: str):
        self.uri = uri
        self.target = string
        self.result = list()
        self.identifiers = [['http', self.http_s], ['/', self.ll], ['//', self.ex_http_s], ['../', self.ex_ll]]
        self.points = [[self.p1, self.p1], [self.p2, self.p2], [self.p3, self.p3]]
        self.process = [-1, 0]  # [pointer to points type, pointer to int1]
        self.temp = [str(), False, str()]
        self.bracket_count = 0
        self.scan()

    def get_add(self):
        result = [None, [], 'No Description Available :(']
        self.temp[0], self.temp[1] = str(), False
        for integer in range(len(self.target) - 2):
            if self.temp[1]:
                if self.target[integer] == self.temp[2]:
                    self.temp[0], self.temp[1] = str(), False
                    for number in range(self.process[1], integer, +1):
                        self.temp[0] += self.target[number]
                    if self.temp[2] == '<':
                        result[0] = self.temp[0]
            else:
                if self.target[integer] + self.target[integer + 1] + self.target[integer + 2] == '<me':
                    self.process[1] = integer + 6
                    self.temp[2] = '>'
                    self.temp[1] = True
                elif self.target[integer] + self.target[integer + 1] + self.target[integer + 2] == '<ti':
                    self.process[1] = integer + 8
                    self.temp[2] = '<'
                    self.temp[1] = True
                elif self.target[integer] + self.target[integer + 1] + self.target[integer + 2] == '</h':
                    return result
        return result

    def scan(self):
        global points
        for integer1 in range(len(self.target)):
            if self.process[0] == -1:
                self.temp[1] = False
                for integer2 in range(3):
                    # noinspection PyArgumentList
                    if self.points[integer2][0](integer1):
                        self.process[0], self.process[1] = integer2, integer1
                        self.temp[1] = True
                        break
            else:
                # noinspection PyArgumentList
                if self.points[self.process[0]][1](integer1):
                    self.temp[0], self.temp[1] = str(), False
                    for number in range(self.process[1] + 1, integer1, +1):
                        self.temp[0] += self.target[number]
                    for identifier in self.identifiers:
                        if self.temp[0].startswith(identifier[0]):
                            # executes the method the identifier points to
                            identifier[1](self.temp[0])
                            self.temp[1], self.process[0], self.process[1] = True, -1, 0
                    if not self.temp[1]:
                        self.sub_scan(self.process[1], integer1)
                        self.process[0], self.process[1] = -1, 0

    def sub_scan(self, pos1, pos2):
        _temp = str()
        for number in range(pos1 + 1, pos2, +1):
            _temp += self.target[number]

        global points
        self.process[0], self.process[1], self.bracket_count = -1, 0, 0
        for integer1 in range(pos1 + 1, pos2, +1):
            if self.process[0] == -1:
                self.temp[1] = False
                for integer2 in range(3):
                    # noinspection PyArgumentList
                    if self.points[integer2][0](integer1):
                        self.process[0], self.process[1] = integer2, integer1
                        self.temp[1] = True
                        break
            else:
                # noinspection PyArgumentList
                if self.points[self.process[0]][1](integer1):
                    self.temp[0], self.temp[1] = str(), False
                    for number in range(self.process[1] + 1, integer1, +1):
                        self.temp[0] += self.target[number]
                    for identifier in self.identifiers:
                        if self.temp[0].startswith(identifier[0]):
                            # executes the method the identifier points to
                            identifier[1](self.temp[0])
                            self.temp[1], self.process[0], self.process[1] = True, -1, 0
                    if not self.temp[1]:
                        self.sub_scan(self.process[1], integer1)
                        self.process[0], self.process[1] = -1, 0

    def http_s(self, target):
        self.result.append(target)
        return ''

    def ll(self, target):  # I call it local link, idk how its named
        temp = [str(), 0]
        for char in self.uri:
            if char == '/':
                temp[1] += 1
                if temp[1] == 3:
                    self.result.append(temp[0] + target)
            temp[0] += char
        self.result.append(temp[0] + target)
        return ''

    def remove_encryption(self, target):  # target is useless and gets thrown into the waste bucket
        return points[self.process[0]][0]

    def ex_http_s(self, target):
        self.result.append("https:" + target)
        return ''

    def ex_ll(self, target):
        temp = [str(), 0]
        for char in self.uri:
            if char == '/':
                temp[1] += 1
                if temp[1] == 3:
                    self.result.append(target.replace('..', ''))
            temp[0] += char
        self.result.append(temp[0] + target.replace('..', ''))
        return ''

    # used for testing, idk when ill delete it
    def __str__(self):
        return f"""{{
            "URL": "{self.uri}",
            "RAW": "{self.target}",
            "DONE": "{self.result}",
            "PROCESS": "{self.process}",
            "TEMP_VARS": "{self.temp}"
        }}"""

    def p1(self, position):
        return True if self.target[position] == '"' and self.target[position - 1] != '\\' else False

    def p2(self, position):
        return True if self.target[position] == '\'' and self.target[position - 1] != '\\' else False

    def p3(self, position):
        if self.target[position] == '(':
            self.bracket_count += 1
            if self.bracket_count == 1:
                return True
        elif self.target[position] == ')':
            self.bracket_count -= 1
            if self.bracket_count == 0:
                return True

    def p4(self, position):
        if len(self.target) > position + 1 and (self.target[position + 1] == '"' or self.target[position + 1] == '\''):
            return False
        if self.target[position] == '=':
            return True

    def p5(self, position):
        return True if self.target[position] == ' ' or self.target[position] == '>' \
                       or self.target[position] == ']' else False

    def get_result(self):
        return self.result

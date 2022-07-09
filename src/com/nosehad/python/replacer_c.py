from com.nosehad.python import url
from com.nosehad.python.url_encrypter_c import UrlENC

points = [['"', '"'], ['\'', '\''], ['(', ')'], ['=', '> ']]  # [<start>, <end>]


class ReplacerHtml:

    def __init__(self, string: str, uri: str, encrypter: UrlENC, pal=False):
        self.encrypter = encrypter
        self.uri = uri
        self.target = string
        self.result = str()
        self.pal = pal
        self.points = [[self.p1, self.p1], [self.p2, self.p2], [self.p3, self.p3]]
        self.process = [-1, 0]  # [pointer to points type, pointer to int1]
        self.temp = [str(), False]
        self.bracket_count = 0
        self.scan()

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
                if not self.temp[1]:
                    self.result += self.target[integer1]
            else:
                # noinspection PyArgumentList
                if self.points[self.process[0]][1](integer1):
                    self.result += self.target[self.process[1]] + self.work(self.process[1] + 1, integer1) + \
                                   self.target[
                                       integer1]
                    self.temp[1], self.process[0], self.process[1] = True, -1, 0
                    if not self.temp[1]:
                        self.result += self.target[self.process[1]] + self.sub_scan(self.process[1], integer1) + \
                                       self.target[integer1]
                        self.process[0], self.process[1] = -1, 0

    def sub_scan(self, pos1, pos2):
        _temp = str()
        for number in range(pos1 + 1, pos2, +1):
            _temp += self.target[number]

        global points
        self.process[0], self.process[1], self.bracket_count = -1, 0, 0
        sub_result = str()
        for integer1 in range(pos1, pos2, +1):
            if self.process[0] == -1:
                self.temp[1] = False
                for integer2 in range(3):
                    # noinspection PyArgumentList
                    if self.points[integer2][0](integer1):
                        self.process[0], self.process[1] = integer2, integer1
                        self.temp[1] = True
                        break
                if not self.temp[1]:
                    sub_result += self.target[integer1]
            else:
                # noinspection PyArgumentList
                if self.points[self.process[0]][1](integer1):
                    sub_result += self.target[self.process[1]] + self.work(self.process[1] + 1, integer1) + self.target[
                        integer1]
                    self.temp[1], self.process[0], self.process[1] = True, -1, 0
                    if not self.temp[1]:
                        sub_result += self.target[self.process[1]] + self.sub_scan(self.process[1], integer1) + \
                                      self.target[integer1]
                        self.process[0], self.process[1] = -1, 0
        return sub_result

    def work(self, start_pos, end_pos) -> str:
        target = str()
        for number in range(start_pos, end_pos, +1):
            target += self.target[number]
        if target.startswith('http'):
            return ("/pal/" if self.pal else "/go/") + self.encrypter.encrypt(target)
        elif target.startswith('/'):
            temp = [str(), 0]
            for char in self.uri:
                if char == '/':
                    temp[1] += 1
                    if temp[1] == 3:
                        return ("/pal/" if self.pal else "/go/") + self.encrypter.encrypt(temp[0] + target)
                temp[0] += char
            return ("/pal/" if self.pal else "/go/") + self.encrypter.encrypt(temp[0] + target)
        elif target.startswith('../'):
            temp = [str(), 0]
            for char in self.uri:
                if char == '/':
                    temp[1] += 1
                    if temp[1] == 3:
                        return ("/pal/" if self.pal else "/go/") + self.encrypter.encrypt(
                            temp[0] + target.replace('..', ''))
                temp[0] += char
            return ("/pal/" if self.pal else "/go/") + self.encrypter.encrypt(
                temp[0] + target.replace('..', ''))
        elif target.endswith('.js') or target.endswith('.css') or target.endswith('.woff') or target.endswith('.woff2'):
            temp = [str(), 0]
            for char in self.uri:
                if char == '/':
                    temp[1] += 1
                    if temp[1] == 3:
                        return ("/pal/" if self.pal else "/go/") + self.encrypter.encrypt(
                            temp[0] + '/' + target)
                temp[0] += char
            return ("/pal/" if self.pal else "/go/") + self.encrypter.encrypt(
                temp[0] + '/' + target)
        elif target.startswith('//'):
            return ("/pal/" if self.pal else "/go/") + self.encrypter.encrypt("https:" + target)
        elif target.startswith('sha512') or target.startswith('sha384') or target.startswith('sha256'):
            return points[self.process[0]][0]
        else:
            return self.sub_scan(pos1=start_pos, pos2=end_pos)

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

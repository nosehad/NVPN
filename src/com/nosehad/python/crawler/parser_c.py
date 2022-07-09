class Parser:
    def __init__(self, string):
        self.parse(string + ' ')

    def parse(self, string):
        temp = [False, 0, 0, False]
        for integer in range(len(string)-1):
            if not temp[0]:
                if string[integer] == '\'' or string[integer] == '"':
                    temp[0], temp[1], temp[2] = True, 1, integer
                if string[integer] == '=' and string[integer+1] != '"' or string[integer+1] != '\'':
                    temp[0], temp[1], temp[2] = True, 0, integer
            else:
                if temp[1] == 1 and string[integer] == '\'' or string[integer] == '"':
                    _temp = str()
                    for number in range(temp[2], integer, +1):
                        _temp += string[number]

                elif temp[1] == 0 and string[integer] == ' ':
                    _temp = str()
                    for number in range(temp[2], integer, +1):
                        _temp += string[number]

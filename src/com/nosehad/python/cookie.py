class Cookie:
    def __init__(self, setter):
        self.add = list()
        self.rem = list()
        for piece in setter.lower().split('; '):
            if piece.startswith('expires') or piece.startswith('max-age') or piece.startswith('domain') or piece.startswith('secure'):
                continue
            elif piece.startswith('path'):
                _res = piece.split(', ')
                if len(_res) == 1:
                    continue
                _res = _res[1].split('=')
                if _res[1] == '' or _res[1] == 'deleted':
                    self.rem.append(_res[0])
                    continue
                self.add.append([_res[0], _res[1]])
                continue
            _res = piece.split('=')
            if len(_res) == 1 or _res[1] == '' or _res[1] == 'deleted':
                self.rem.append(_res[0])
                continue
            self.add.append([_res[0], _res[1]])

    def get_cookies(self):
        return [self.add, self.rem]

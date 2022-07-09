def contains_illegal(string: str, illegal: str = ',;+~\?}][{&%$§"!<> '):
    for ch1 in string:
        for ch2 in illegal:
            if ch1 == ch2:
                return True
    return False


def is_url(string: str):
    return False if not string.startswith('https://') or '.' not in string else True


def is_email(string: str):
    return False if '.' not in string or '@' not in string or contains_illegal(string) else True

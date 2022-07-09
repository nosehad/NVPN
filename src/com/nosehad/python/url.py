def is_url(string: str):
    return False if not string.startswith('https://') or string.startswith('http://') else True


def get_raw(url):
    res = str()
    integer = 0
    for char in url:
        if char == '/':
            integer += 1
            if integer == 3:
                return res
        res += char
    return res


# TODO: make faster
def get_extension(url):
    uncommon_file_extensions = ['min.css', 'bundle.css', 'min.js', 'bundle.js']
    common_file_extensions = ['js', 'css', 'ico', 'png', 'jpeg', 'svg', 'json', 'webp', 'ttf',
                              'woff2', 'woff', 'mp4', 'jpeg', 'exe', 'zip', 'dll']
    for file_extension in uncommon_file_extensions:
        if url.endswith(file_extension):
            return '.' + file_extension
    for file_extension in common_file_extensions:
        if url.endswith(file_extension):
            return '.' + file_extension
    return ''


def get_content_type(url):
    content_types = [['min.js', 'application/javascript; charset=utf-8'], ['min.css', 'text/css; charset=utf-8'],
                     ['js', 'application/javascript'], ['css', 'text/css'], ['svg', 'image/svg+xml'],
                     ['json', 'application/xml'], ['png', 'image/png'], ['ico', 'image/x-icon'], ['webp', 'image/webp'],
                     ['ttf', 'application/font-stnf'], ['woff2', 'font/woff2'], ['mp4', 'video/mp4'],
                     ['jpeg', 'image/jpeg'], ['woff', 'application/font-woff'], ['exe', 'media/download'],
                     ['zip', 'media/download'], ['dll', 'media/download']]
    for content_type in content_types:
        if url.endswith(content_type[0]):
            return content_type[1]
    return None


def after(string, pos):
    result = str()
    for integer in range(len(string) - 1, pos, -1):
        result = string[integer] + result
    return result


def has_extension(url):
    common_file_extensions = ['min.css', 'min.js', 'js', 'css', 'ico', 'png', 'jpeg', 'svg', 'json', 'webp', 'ttf',
                              'woff2', 'woff', 'mp4', 'jpeg', 'exe', 'zip', 'dll']
    for file_extension in common_file_extensions:
        if url.endswith(file_extension):
            return True
    return False


def contains_illegal(url):
    illegal = [',', ' ', '^']
    for char1 in url:
        for char2 in illegal:
            if char1 == char2:
                return True
    return False

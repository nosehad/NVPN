import os
import random

from flask import Flask, jsonify, make_response, send_from_directory, request

from com.nosehad.python import user_c as ulib, url
from com.nosehad.python import utils
from com.nosehad.python.logger import Logger
from com.nosehad.python.map_c import Map
from com.nosehad.python.server_c import Server
from com.nosehad.python.session_server import Sessions
from com.nosehad.python.url_decrypter_c import UrlDEC
from com.nosehad.python.url_encrypter_c import UrlENC
from com.nosehad.python.user_c import User

# logger, because I have to log ip addresses in some cases
LOGGER = Logger()

# flask instance
# Flask is an web framework, this is based on
APP = Flask(__name__, static_url_path="")

# this will be more dynamic and reflexive in the future
SERVER = Server()

# ip and browser specific sessions
SESSIONS = Sessions()
UCACHE: Map = Map()

PUBLIC_USER = User(nocon=True)
# assigning user values manually, to skip slow constructor
PUBLIC_USER.email, PUBLIC_USER.encrypter, PUBLIC_USER.decrypter, PUBLIC_USER.cookies = '-1', UrlENC(-2), UrlDEC(-2), []

URL = 'http://127.0.0.1'


@APP.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@APP.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.route('/temp/<data>', methods=['GET'])
def get_file(data):
    return send_from_directory(os.path.join(APP.root_path, 'assets'), data)


@APP.route('/browser', methods=['GET'])
def get_browser():
    return make_response(SERVER.get_bview())


@APP.route('/favicon.ico')
def get_favicon():
    return get_image('favicon.ico')


@APP.route('/images/<data>', methods=['GET'])
def get_image(data):
    return send_from_directory(os.path.join(APP.root_path, 'assets'),
                               data)


@APP.route('/', methods=['GET'])
def render_home():
    if UCACHE.contains(request.remote_addr):
        return make_response(SERVER.get_page('home', UCACHE.get(request.remote_addr)))
    return make_response(SERVER.get_page('home'))


@APP.route('/l/<data>', methods=['GET'])
def get_result1(data: str):
    checked = 0
    res = ['404', 1]
    for session in SESSIONS.get_sessions(request.remote_addr):
        if session == 'banned':
            return 'banned'
        elif 'sus=' in session:
            checked = 1
            SESSIONS.replace_session(request.remote_addr, session,
                                     'sus=' + str(int(session.replace('sus=', '')) + 1))
    if not checked:
        SESSIONS.add_session(request.remote_addr, 'sus=1')

    if data == 'is':
        if UCACHE.contains(request.remote_addr):
            res[0] = 'true'
            res[1] = 0
        else:
            res[1] = 0
            res[0] = 'false'

    elif data == 'new':
        res[1] = 0
        f = False
        for session in SESSIONS.get_sessions(request.remote_addr):
            if session == 'newu':
                SESSIONS.remove_session(request.remote_addr, 'newu')
                res[0] = '1'
                f = True
                break
            elif session == 'newl':
                SESSIONS.remove_session(request.remote_addr, 'newl')
                res[0] = '2'
                f = True
                break
        if not f:
            res[0] = '3'

    elif data == 'logout':
        LOGGER.log(f'{request.remote_addr} logged out from {UCACHE.get(request.remote_addr)}.')
        UCACHE.remove(request.remote_addr)

    elif data.startswith('get='):
        _data = data.replace('get=', '').replace('&2F', '/').replace('&3F', '?')
        res[1] = 0
        if url.is_url(_data): res[0] = f'{URL}/pal/{PUBLIC_USER.get_encrypter().encrypt(_data)}'
        else: res[0] = 'error: DAU'

    elif data.startswith('do='):
        if UCACHE.contains(request.remote_addr):
            res[0] = 'alr'
        _data = data.replace('do=', '').split('&&')
        if len(_data) != 2:
            res[0] = 'failure'
        elif ulib.valid(_data[0], _data[1]):
            # log ip address and username
            LOGGER.log(f'{request.remote_addr} logged in as {_data[0]}.')
            UCACHE.add(request.remote_addr, User(_data[0], int(random.random() * 10000000000000)))
            SESSIONS.add_session(request.remote_addr, 'newl')
            return make_response('done')
        else:
            res[0] = 'failure'

    elif data.startswith('create='):
        _data = data.replace('create=', '').split('&&')
        if len(_data) < 2:
            res[0] = 'failure'
        elif not utils.is_email(_data[0]):
            res[0] = 'email'
        elif ulib.confirm(_data[0]):
            ulib.create(_data[0], _data[1])
            UCACHE.add(request.remote_addr, User(_data[0], int(random.random() * 10000000000000)))
            # log ip address and username
            LOGGER.log(f'{request.remote_addr} logged in as {_data[0]}.')
            SESSIONS.add_session(request.remote_addr, 'newu')
            res[0] = 'done'
            res[1] = 0
        else:
            res[0] = 'failure'
    for session in SESSIONS.get_sessions(request.remote_addr):
        if 'sus=' in session and res[1] == 0:
            SESSIONS.replace_session(request.remote_addr, session,
                                     'sus=0')
            break
        elif session == 'sus=3':
            SESSIONS.replace_session(request.remote_addr, 'sus=3', 'banned')
            break
    return make_response(res[0])


@APP.route('/go/<data1>', methods=['GET', 'POST'])
def render_result(data1, data2=None, data3=None, data4=None, data5=None):
    usr = UCACHE.get(request.remote_addr)

    additional = [data2, data3, data4, data5]
    while None in additional: additional.remove(None)
    if usr is None:
        res = SERVER.get(data1, user=None)
        resp = make_response(res[0])
        for header in res[1]:
            resp.headers[header[0]] = header[1]
        return resp
    res = SERVER.get(data1, usr, additional)
    resp = make_response(res[0])
    if res[1] is not None:
        resp.headers[res[1][0]] = res[1][1]
    return resp


@APP.route('/pal/<data1>', methods=['GET', 'POST'])
def render_default_result(data1):
    res = SERVER.get(data1, user=PUBLIC_USER, pal=True)
    resp = make_response(res[0])
    for header in res[1]:
        resp.headers[header[0]] = header[1]
    return resp


@APP.route('/<data>', methods=['GET'])
def render(data):
    if data == 'go':
        return render_result(None, None, None, None, None)

    usr = UCACHE.get(request.remote_addr)

    if usr is None:
        return make_response(SERVER.get_page(data))
    return make_response(SERVER.get_page(data, usr, request.args))


if __name__ == '__main__':
    APP.run(port=80, debug=True)

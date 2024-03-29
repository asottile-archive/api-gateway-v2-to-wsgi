from __future__ import annotations

import json
import os.path
import sys

import flask
import pytest

import api_gateway_v2_to_wsgi

HERE = os.path.abspath(os.path.dirname(__file__))

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return f'''\
GET
full url: {flask.url_for("index", _external=True)}
a header: {flask.request.headers.getlist('a')}
b header: {flask.request.headers.getlist('b')}
'''


@app.route('/', methods=['POST'])
def post_index():
    return f'''\
POST
data: {flask.request.data!r}
'''


@app.route('/wat')
def query_route():
    return f'''\
wat route
x param: {flask.request.args.getlist('x')}
y param: {flask.request.args.getlist('y')}
'''


@app.route('/cookie')
def cookies_route():
    return f'''\
cookies route
a cookie: {flask.request.cookies.get('a')!r}
b cookie: {flask.request.cookies.get('b')!r}
'''


@app.route('/image.gif')
def image_route():
    return flask.Response(
        b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9'
        b'\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02D\x01\x00;',
        mimetype='image/gif',
    )


handler = api_gateway_v2_to_wsgi.make_lambda_handler(app)


def _event(name):
    with open(os.path.join(HERE, f'../testing/data/{name}.json')) as f:
        return json.load(f)


def test_get_request():
    resp = handler(_event('get'), {})
    expected_body = '''\
GET
full url: https://kr8spsb5ti.execute-api.us-east-1.amazonaws.com/
a header: []
b header: []
'''
    assert resp == {
        'statusCode': 200,
        'isBase64Encoded': False,
        'body': expected_body,
        'headers': {
            'Content-Length': '96',
            'Content-Type': 'text/html; charset=utf-8',
        },
    }


def test_post_request():
    resp = handler(_event('post'), {})
    expected_body = '''\
POST
data: b'hi'
'''
    assert resp == {
        'statusCode': 200,
        'isBase64Encoded': False,
        'body': expected_body,
        'headers': {
            'Content-Length': '17',
            'Content-Type': 'text/html; charset=utf-8',
        },
    }


def test_query_string():
    resp = handler(_event('query'), {})
    expected_body = '''\
wat route
x param: ['1', '2']
y param: ['3']
'''
    assert resp == {
        'statusCode': 200,
        'isBase64Encoded': False,
        'body': expected_body,
        'headers': {
            'Content-Length': '45',
            'Content-Type': 'text/html; charset=utf-8',
        },
    }


def test_multi_headers():
    resp = handler(_event('headers'), {})
    # XXX: amazon bumbles mutli-headers into a single value
    expected_body = '''\
GET
full url: https://kr8spsb5ti.execute-api.us-east-1.amazonaws.com/
a header: ['1,2']
b header: ['3']
'''
    assert resp == {
        'statusCode': 200,
        'isBase64Encoded': False,
        'body': expected_body,
        'headers': {
            'Content-Length': '104',
            'Content-Type': 'text/html; charset=utf-8',
        },
    }


def test_raising_error():
    # flask doesn't do this, so we make a silly app that does
    try:
        raise AssertionError('wat')
    except AssertionError:
        exc_info = sys.exc_info()

    def app(environ, handle_response):
        handle_response('500 error', [], exc_info=exc_info)

    error_app = api_gateway_v2_to_wsgi.make_lambda_handler(app)

    with pytest.raises(AssertionError) as excinfo:
        error_app(_event('get'), {})

    msg, = excinfo.value.args
    assert msg == 'wat'


def test_cookies():
    resp = handler(_event('cookies'), {})
    expected_body = '''\
cookies route
a cookie: '1'
b cookie: '2'
'''
    assert resp == {
        'statusCode': 200,
        'isBase64Encoded': False,
        'body': expected_body,
        'headers': {
            'Content-Length': '42',
            'Content-Type': 'text/html; charset=utf-8',
        },
    }


def test_binary_reposnse():
    resp = handler(_event('image'), {})
    assert resp == {
        'statusCode': 200,
        'isBase64Encoded': True,
        'body': 'R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==',
        'headers': {
            'Content-Length': '43',
            'Content-Type': 'image/gif',
        },
    }

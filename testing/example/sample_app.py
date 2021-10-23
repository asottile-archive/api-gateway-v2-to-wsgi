import flask

import api_gateway_v2_to_wsgi

app = flask.Flask(__name__)


@app.route('/')
def home() -> str:
    return 'hello hello world'


@app.route('/u/<username>')
def profile(username: str) -> str:
    return f'hello hello {username}'


@app.route('/image.gif')
def image_route() -> flask.Response:
    return flask.Response(
        b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9'
        b'\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02D\x01\x00;',
        mimetype='image/gif',
    )


lambda_handler = api_gateway_v2_to_wsgi.make_lambda_handler(app)


def main() -> int:
    app.run(port=8001)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

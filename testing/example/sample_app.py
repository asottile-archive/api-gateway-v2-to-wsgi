import flask

import api_gateway_v2_to_wsgi

app = flask.Flask(__name__)


@app.route('/')
def home() -> str:
    return 'hello hello world'


@app.route('/u/<username>')
def profile(username: str) -> str:
    return f'hello hello {username}'


lambda_handler = api_gateway_v2_to_wsgi.make_lambda_handler(app)


def main() -> int:
    app.run(port=8001)
    return 0


if __name__ == '__main__':
    exit(main())

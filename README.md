[![build status](https://github.com/asottile/api-gateway-v2-to-wsgi/actions/workflows/main.yml/badge.svg)](https://github.com/asottile/api-gateway-v2-to-wsgi/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/asottile/api-gateway-v2-to-wsgi/main.svg)](https://results.pre-commit.ci/latest/github/asottile/api-gateway-v2-to-wsgi/main)

api-gateway-v2-to-wsgi
======================

translation from the aws api gateway v2.0 lambda event to wsgi

## installation

```bash
pip install api-gateway-v2-to-wsgi
```

## usage

```python
import api_gateway_v2_to_wsgi

from ... import app

# app is your wsgi callable, such as the `Flask(...)` object from `flask`
lambda_handler = api_gateway_v2_to_wsgi.make_lambda_handler(app)
```

## sample application

for a full sample, see [testing/example](testing/example)

## more information

for more information on how I set up my lambda, see
[testing/example.md](testing/example.md).

additionally, see the [api gateway documentation] (though it's not very good
at the time of writing so glhf)

seems the [lambda integration guide] is slightly better

[api gateway documentation]: https://docs.aws.amazon.com/apigateway/index.html
[lambda integration guide]: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html

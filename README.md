[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/asottile.api-gateway-v2-to-wsgi?branchName=master)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=65&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/65/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=65&branchName=master)

api-gateway-v2-to-wsgi
======================

translation from the aws api gateway v2.0 lambda event to wsgi

## installation

`pip install api-gateway-v2-to-wsgi`

## usage

```python
import api_gateway_v2_to_wsgi

from ... import app

# app is your wsgi callable, such as the `Flask(...)` object from `flask`
lambda_handler = api_gateway_v2_to_wsgi.make_lambda_handler(app)
```

## more information

for more information on how I set up my lambda, see
[testing/example.md](testing/example.md).

additionally, see the [api gateway documentation] (though it's not very good
at the time of writing so glhf)

[api gateway documentation]: https://docs.aws.amazon.com/apigateway/index.html

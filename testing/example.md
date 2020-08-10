### terraform

I used the following terraform to set up my lambda / gateway

```terraform
resource "aws_lambda_function" "web" {
  function_name = "web"
  ...
  role          = aws_iam_role.lambda_web.arn
  handler       = "lambda_web.lambda_handler"
  runtime       = "python3.8"
}

resource "aws_apigatewayv2_api" "web_gateway" {
  name          = "web_gateway"
  protocol_type = "HTTP"
  target        = aws_lambda_function.web.arn
}

resource "aws_lambda_permission" "web_gateway" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.web.arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.web_gateway.execution_arn}/*/*"
}
```

### sample app

I used this dummy app to get the sample events

```python
lambda_handler = lambda event, context: event
```

### requests

```bash
BASE=https://kr8spsb5ti.execute-api.us-east-1.amazonaws.com
curl "$BASE" | jq . > testing/data/get.json
curl -XPOST -H 'content-type:' -d 'hi' "$BASE" | jq . > testing/data/post.json
curl "$BASE/wat?x=1&x=2&y=3" | jq . > testing/data/query.json
curl -H 'a: 1' -H 'a: 2' -H 'b: 3' "$BASE" | jq . > testing/data/headers.json
```

sample-app
==========

this is a sample application using `flask` and this library to serve a lambda
in aws

## running this example

you can set up this application using the terraform provided in [./tf](./tf)

### initializing and creating the aws infrastructure

the first step is to set up the terraform infrastructure.

this creates a few things:
- the necessary iam roles your lambda will use
- a placeholder lambda (that always crashes)
- the api gateway to connect to your lambda

```bash
cd tf
terraform init
terraform apply
cd ..
```

you'll answer "yes" to the prompt and your output will look something like
this:

```console
$ terraform apply

...

  Enter a value: yes

aws_iam_role.sample_app: Creating...
aws_iam_policy.sample_app_permissions_policy: Creating...
aws_iam_role.sample_app: Creation complete after 1s [id=sample_app]
aws_lambda_function.sample_app: Creating...
aws_iam_policy.sample_app_permissions_policy: Creation complete after 1s [id=arn:aws:iam::952911408644:policy/terraform-20200810034840168600000001]
aws_iam_role_policy_attachment.sample_app_permissions_policy_attach: Creating...
aws_iam_role_policy_attachment.sample_app_permissions_policy_attach: Creation complete after 1s [id=sample_app-20200810034841916100000002]
aws_lambda_function.sample_app: Still creating... [10s elapsed]
aws_lambda_function.sample_app: Creation complete after 16s [id=sample_app]
aws_apigatewayv2_api.sample_app_gateway: Creating...
aws_apigatewayv2_api.sample_app_gateway: Creation complete after 2s [id=l45ezct9w4]
aws_lambda_permission.sample_app_gateway: Creating...
aws_lambda_permission.sample_app_gateway: Creation complete after 1s [id=terraform-20200810034859413700000003]

Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

Outputs:

api_gateway_address = "https://l45ezct9w4.execute-api.us-east-1.amazonaws.com"
```

the important part of this is the `api_gateway_address` portion, we'll be
using that later!

### trying out the gateway

now that the infrastructure is set up we should be able to try out the
gateway!  using the value from before, we'll curl the api gateway we created:

```console
$ curl https://l45ezct9w4.execute-api.us-east-1.amazonaws.com/ && echo
{"message":"Internal Server Error"}
```

hmmm right, we forgot to actually set up the lambda!

### build the lambda

there's a small build script which'll create the necessary lambda zip to upload

```bash
./make-lambda
```

this'll spit out some pip output and then create `out.zip`

### uploading the lambda

to change the lambda code, you'll push that zip to aws

```bash
aws lambda update-function-code \
    --function-name sample_app \
    --zip-file fileb://out.zip
```

### trying the app again

```console
$ curl https://l45ezct9w4.execute-api.us-east-1.amazonaws.com/ && echo
hello hello world
```

success!

you can also try the other endpoint:

```console
$ curl https://l45ezct9w4.execute-api.us-east-1.amazonaws.com/u/asottile && echo
hello hello asottile
```

### destroying the app

ok demo complete!  time to delete everything:

```bash
cd tf
terraform destroy
cd ..
```

### placeholder app

I used this placeholder app to get the sample events

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
curl -H 'cookie: a=1;b=2' "$BASE/cookie" | jq . > testing/data/cookies.json
```

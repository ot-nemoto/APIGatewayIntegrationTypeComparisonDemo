# AnyResponseCodeByAwsProxyDemo

## 概要

- [AnyResponseCodeDemo](https://github.com/ot-nemoto/AnyResponseCodeDemo)で指定したレスポンスコードをAPI Gatewayから返却する方法のデモを、統合リクエストで**Lambdaプロキシ統合**を使用した場合に、API GatewayおよびLambdaでの記述内容等の差異を検証したデモ

## 構成

- クエリパラメータ *expect_code* で指定したレスポンスコードを指定します。
- 未指定の場合は、デフォルトでは **200** を返します。
- *expect_code*=**200**

```py
# json を return
return {
  "statusCode": 200,
  "body": json.dumps({
    "message": "hello world"
  })
}
```

API Gateway では **statusCode** でレスポンスコードを判断し、**body**の内容を返却する。
この場合、bodyはString形式にして返却する必要がある。

```json
{
  "message": "hello world"
}
```

- *expect_code*=**400**

```py
# Exceptionを発生
return {
  "statusCode": 400,
  "body": json.dumps({
    "message": "Bad Request"
  })
}
```

レスポンスコードを **statusCode** に設定し、返却したい値を **body** に文字列で指定する。
他のレスポンスコードについても同様。

```json
{
  "message": "Bad Request"
}
```

## デプロイ

ソースコードをアップロードするS3バケットを作成

```sh
S3BUCKET=any-response-code-by-aws-proxy-demo-bucket-`date +%Y%m%d%H%M%S`
echo ${S3BUCKET}
  # any-response-code-by-aws-proxy-demo-bucket-01234567890123

aws s3 mb s3://${S3BUCKET}
  # make_bucket: any-response-code-by-aws-proxy-demo-bucket-01234567890123
```

パッケージ

```sh
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket ${S3BUCKET}
```

デプロイ

```sh
sam deploy \
    --template-file packaged.yaml \
    --stack-name any-response-code-by-aws-proxy-demo \
    --capabilities CAPABILITY_IAM
```

## 使い方

URLを取得

```sh
INVOKE_URL=$(aws cloudformation describe-stacks \
    --stack-name any-response-code-by-aws-proxy-demo \
    --query 'Stacks[].Outputs[?OutputKey==`InvokeUrl`].OutputValue' \
    --output text)
echo ${INVOKE_URL}
  #
```

正常なレスポンスコードを返すリクエスト

```sh
curl -s ${INVOKE_URL} | jq
  # {
  #   "body": {
  #     "message": "hello world"
  #   },
  #   "statusCode": 200
  # }
curl -s ${INVOKE_URL} -o /dev/null -w '%{http_code}\n'
  # 200
```

*expect_code* で期待するHTTPレスポンスコードを指定するリクエスト

```sh
curl -s ${INVOKE_URL}?expect_code=400 | jq
  # {
  #   "statusCode": 400,
  #   "body": {
  #     "message": "Bad Request"
  #   }
  # }
curl -s ${INVOKE_URL}?expect_code=400 -o /dev/null -w '%{http_code}\n'
  # 400
```

## お掃除

```sh
aws cloudformation delete-stack \
    --stack-name any-response-code-by-aws-proxy-demo

aws s3 rb s3://${S3BUCKET} --force
  # ...
  # delete: s3://any-response-code-by-aws-proxy-demo-bucket-01234567890123/...
  # remove_bucket: any-response-code-by-aws-proxy-demo-bucket-01234567890123
```

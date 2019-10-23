# IntegrationTypeCompDemo

## 概要

## 構成

## デプロイ

ソースコードをアップロードするS3バケットを作成

```sh
S3BUCKET=integration-type-comp-demo-bucket-`date +%Y%m%d%H%M%S`
echo ${S3BUCKET}
  # integration-type-comp-demo-bucket-01234567890123

aws s3 mb s3://${S3BUCKET}
  # make_bucket: integration-type-comp-demo-bucket-01234567890123
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
    --stack-name integration-type-comp-demo \
    --capabilities CAPABILITY_IAM
```

## 使い方

## クリーンアップ

```sh
aws cloudformation delete-stack \
    --stack-name integration-type-comp-demo

aws s3 rb s3://${S3BUCKET} --force
  # ...
  # delete: s3://integration-type-comp-demo-bucket-01234567890123/...
  # remove_bucket: integration-type-comp-demo-bucket-01234567890123
```

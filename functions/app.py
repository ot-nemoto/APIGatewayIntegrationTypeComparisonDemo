# coding: UTF-8

import json

def lambda_handler(event, context):
  print(json.dumps(event))

  queryStringParameters = event.get('queryStringParameters') \
    if event.get('queryStringParameters') is not None else {}
  expect_code = queryStringParameters.get('expect_code', '200')
  try:
    if expect_code == '200':
      return {
        "statusCode": expect_code,
        "body": json.dumps({
          "message": "hello world"
        })
      }
    elif expect_code == '400':
      raise Exception("Bad Request")
    elif expect_code == '401':
      return {
        "statusCode": 200,
        "body": json.dumps({
          "stackTrace": [],
          "errorType": "Exception",
          "errorMessage": "Unauthorixed"
        })
      }
    elif expect_code == '403':
      raise Exception("あなたにはアクセス権がありません")
    else:
      expect_code = 500
      raise Exception("Internal Server Error")
  except Exception as e:
    print(e.message)
    return {
      "statusCode": expect_code,
      "body": json.dumps({
        "message": e.message
      })
    }

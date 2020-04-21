import os
import json
import requests
import urllib

from base64 import b64encode, b64decode
import hashlib
import hmac

from requests.structures import CaseInsensitiveDict


API_ID = os.environ.get("API_ID")  # API ID
SERVER_API_CONSUMER_KEY = os.environ.get("SERVER_API_CONSUMER_KEY")  # Server API Consumer Key
BOTNO = os.environ.get("BOTNO")  # Bot No

TOKEN = os.environ.get("LW_TOKEN")  # 発行したToken


def validate_request(body, signature):
    """
    リクエスト検証
    """
    # API IDを秘密鍵に利用
    secretKey = API_ID.encode()
    payload = body.encode()

    # HMAC-SHA256 アルゴリズムでエンコード
    encoded_body = hmac.new(secretKey, payload, hashlib.sha256).digest()
    # BASE64 エンコード
    encoded_b64_body = b64encode(encoded_body).decode()

    # 比較
    return encoded_b64_body == signature


def send_message(content, account_id):
    """
    送信
    """
    url = 'https://apis.worksmobile.com/' + API_ID + '/message/sendMessage/v2'
    headers = {
          'Content-Type' : 'application/json;charset=UTF-8',
          'consumerKey' : SERVER_API_CONSUMER_KEY,
          'Authorization' : "Bearer " + TOKEN
        }
    params = {
            "botNo" : int(BOTNO),
            "accountId" : account_id,
            "content" : content
        }

    form_data = json.dumps(params)

    r = requests.post(url=url, data=form_data, headers=headers)
    if r.status_code == 200:
        return True

    return False


def handler(event, context):
    """
    チャットボット処理
    """
    event = CaseInsensitiveDict(event)
    headers = event["headers"]
    body = event["body"]

    # リクエスト検証
    if not validate_request(body, headers.get("x-works-signature")):
        # 不正なリクエスト
        return

    # Jsonへパース
    request = json.loads(body)

    # 送信ユーザー取得
    account_id = request["source"]["accountId"]

    res_content = {
        "type" : "text",
        "text" : "テキストのみ対応"
    }

    # 受信したメッセージの中身を確認
    request_type = request["type"]
    ## Message
    if request_type == "message":
        content = request["content"]
        content_type = content["type"]
        ## Text
        if content_type == "text":
            text = content["text"]
            if text in "こんにちは":
                res_content = {
                    "type" : "text",
                    "text" : "こんにちは！"
                }
            else:
                res_content = {
                    "type" : "text",
                    "text" : "・・・"
                }

    # 送信
    rst = send_message(res_content, account_id)

    res_body = {
        "code": 200,
        "message": "OK"
    }
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(res_body)
    }

    return response

import os
import json
import jwt
import requests
import urllib
import datetime


SERVER_LIST_ID = ""  # Server List ID
SERVER_LIST_PRIVATEKEY = "" # Server List Private Key
API_ID = ""  # API ID


def get_jwt():
    """
    JWTの生成
    """
    current_time = datetime.datetime.now().timestamp()

    iss = SERVER_LIST_ID
    iat = current_time
    exp = current_time + 3600 # 1時間有効
    secret = SERVER_LIST_PRIVATEKEY

    jwstoken = jwt.encode(
        {
            "iss": iss,
            "iat": iat,
            "exp": exp
        }, secret, algorithm="RS256")

    return jwstoken.decode('utf-8')


def get_server_token(jwttoken):
    """
    Token発行
    """
    url = 'https://authapi.worksmobile.com/b/' + API_ID + '/server/token'
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    params = {
        "grant_type" : urllib.parse.quote("urn:ietf:params:oauth:grant-type:jwt-bearer"),
        "assertion" : jwttoken
    }

    form_data = params

    r = requests.post(url=url, data=form_data, headers=headers)

    body = json.loads(r.text)
    access_token = body["access_token"]

    return access_token


if __name__ == "__main__":
    jwttoken = get_jwt()
    access_token = get_server_token(jwttoken)

    print(access_token)

import json
import time

import requests

import push
from AES import Encrypt


def getToken(get_token_user: dict, Ua) -> dict:  # 用户信息 UA
    # time.sleep(5)
    global res
    print("    获取Token", end="    ")
    headers: dict = {
        "content-type": "application/json; charset=utf-8",
        "accept-encoding": "gzip",
        "content-length": "213",
        "host": "api.moguding.net:9000",
        # "UserAgent": Ua
    }
    data: dict = {
        "phone": Encrypt("23DbtQHR2UMbH6mJ", get_token_user["phone"]),
        "password": Encrypt("23DbtQHR2UMbH6mJ", get_token_user["password"]),
        "captcha": "null",
        "loginType": "android",
        "uuid": "",
        "device": "android",
        "version": "5.5.0",
        "t": Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000))),
    }
    try:
        res = requests.post(url="https://api.moguding.net:9000/session/user/v3/login", data=json.dumps(data),
                            headers=headers).json()

        print("    请求成功\n", end="")
    except:
        print("    请求失败")
        return {
            "sign": "请求失败",
            "position": "getToken",
            "characteristic_push": push.push(push_user=get_token_user, createTime="请手动签到")
        }

    if res['code'] == 200:
        return {
            "token": res["data"]["token"],
            "userId": res["data"]["userId"]
        }
    else:
        print(f"\n    错误原因  {res['msg']}")
        return {
            "sign": res['msg'],
            "position": "getToken",
            "characteristic_push": push.push(push_user=get_token_user, createTime="请手动签到")
        }

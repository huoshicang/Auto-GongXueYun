import json
import time

import requests

import AES


def sign_in_count(sign_in_count_user: dict, ) -> dict:  # 用户信息 Ua
    # def sign_in_count() -> dict:  # 用户信息 Ua
    # time.sleep(5)
    global res
    header: dict = {
        "accept-encoding": "gzip",
        "content-length": "84",
        "rolekey": "student",
        "host": "api.moguding.net:9000",
        # "user-agent": GetUserAgent,
        "authorization": sign_in_count_user["token"],
        "userid": sign_in_count_user["userId"],
        "content-type": "application/json;charset=UTF-8",
    }

    data: dict = {
        "planId": sign_in_count_user["planId"],
        "t": AES.Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000)))
    }
    try:
        res = requests.post(url="https://api.moguding.net:9000/attendence/clock/v1/countByPlan", headers=header,
                            data=json.dumps(data)).json()
        print("    请求成功\n", end="")
        print(res)
        return res["data"]
    except:
        print("    请求失败")

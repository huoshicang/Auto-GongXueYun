import json
import time

import requests

import AES
import push


def GetConfirmCheck(confirm_check_user: dict, Ua) -> dict:  # 用户信息 Ua
    # time.sleep(5)
    global res
    print("    获取签到日志", end="  ")
    header: dict = {
        "accept-encoding": "gzip",
        "content-type": "application/json;charset=UTF-8",
        "rolekey": "student",
        "host": "api.moguding.net:9000",
        "authorization": confirm_check_user["token"],
        # "user-agent": Ua,
        "userid": confirm_check_user["userId"],
        "content-length": "111",
    }
    data: dict = {
        "currPage": 1,
        "pageSize": 10,
        "planId": confirm_check_user["planId"],
        "t": AES.Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000)))
    }
    try:
        res = requests.post(url="https://api.moguding.net:9000/attendence/clock/v1/list", headers=header,
                            data=json.dumps(data)).json()

        print("    请求成功\n", end="")
        return res['data'][0]
    except:
        print("    请求失败")
        return {
            "sign": "请求失败",
            "position": "确认签到",
            "characteristic_push": push.push(push_user=confirm_check_user, createTime="请手动签到")
        }

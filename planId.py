import json
import time

import requests

import AES
import push
from md5 import Md5


def GetPlanId(get_planid_user: dict, Ua) -> dict:  # 用户信息 Ua
    # time.sleep(5)
    global res
    print("    获取PlanId", end="    ")
    data: dict = {
        # "pageSize": 999999,
        "t": AES.Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000))),
    }
    headers: dict = {
        "userid": get_planid_user['userId'],
        "accept-encoding": "gzip",
        "content-length": "58",
        "rolekey": "student",
        "host": "api.moguding.net:9000",
        "authorization": get_planid_user['token'],
        "content-type": "application/json; charset=utf-8",
        "sign": Md5(f'{get_planid_user["userId"]}student'),
        # "UserAgent": Ua
    }
    try:
        res = requests.post(url="https://api.moguding.net:9000/practice/plan/v3/getPlanByStu", data=json.dumps(data),
                            headers=headers, ).json()

        print("    请求成功\n", end="")
    except:
        print("    请求失败")
        return {
            "sign": "请求失败",
            "position": "getPlanId",
            "characteristic_push": push.push(push_user=get_planid_user, createTime="请手动签到")
        }

    if res["code"] == 200:
        return {
            'planId': res['data'][0]['planId']
        }
    else:
        print(f"\n    错误原因  {res['msg']}")
        return {
            "sign": res['msg'],
            "position": "getPlanId",
            "characteristic_push": push.push(push_user=get_planid_user, createTime="请手动签到")
        }

import datetime
import json
import time

import requests

import AES
import push


def SignRecord(sign_record_user: dict, Ua) -> dict:  # 用户信息 Ua
    # time.sleep(5)
    global res
    print("    获取签到记录", end="  ")
    header: dict = {
        "accept-encoding": "gzip",
        "content-type": "application/json;charset=UTF-8",
        "rolekey": "student",
        "host": "api.moguding.net:9000",
        "authorization": sign_record_user["token"],
        # "user-agent": Ua
    }
    data: dict = {
        # "startTime": "2022-08-20 00:00:00",
        # "endTime": "2023-03-20 00:00:00",
        "t": AES.Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000)))
    }
    try:
        res = requests.post(url="https://api.moguding.net:9000/attendence/clock/v1/listSynchro", headers=header,
                            data=json.dumps(data)).json()

        print("    请求成功\n", end="")
    except:
        print("    请求失败")
        return {
            "sign": "请求失败",
            "position": "记录",
            "characteristic_push": push.push(push_user=sign_record_user, createTime="请手动签到")
        }
    if "token失效" == res['msg']:
        print("    token失效")
        return {
            "sign": "token失效",
            "position": "",
            "characteristic_push": ''
        }
    elif res['data'] == [] or res['data'] is None or res['data'] == '':
        print("    没签过")
        return {
            "sign": "没签过",
            "position": "",
            "characteristic_push": ''
        }
    elif str(datetime.date.today()) == res['data'][0]['dateYmd']:
        print("    不需要签到")
        # return {
        #     "sign": "需要签到",
        #     "position": "",
        #     "characteristic_push": ''
        # }
        return {
            "sign": "不需要签到",
            "position": "",
            "characteristic_push": '不推送'
        }
    else:
        print("    需要签到")
        return {
            "sign": "需要签到",
            "position": "",
            "characteristic_push": ''
        }

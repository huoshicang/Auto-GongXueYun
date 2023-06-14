import datetime
import json
import time

import requests

import AES
import mysql
import push
from md5 import Md5


def Writ(writ_user: dict, save_time: str) -> None:
    print("  写入数据库：签到时间")
    sql = f"""UPDATE users SET time="{save_time}" WHERE name = '{writ_user["name"]}';"""
    mysql.update(sql=sql)


def Save(save_user, Ua):
    # time.sleep(5)
    print("    开始签到", end="    ")
    global res
    headers: dict = {
        'roleKey': 'student',
        # "user-agent": Ua,
        "sign": Md5(text='Android' + 'START' + save_user['planId'] + save_user['userId'] + save_user['address']),
        "authorization": save_user["token"],
        "content-type": "application/json; charset=UTF-8",
        "userid": save_user['userId']
    }
    data: dict = {
        # 国家
        "country": save_user["country"],
        # 详细地址
        "address": save_user["address"],
        # 省
        "province": save_user["province"],
        # 市
        "city": save_user["city"],
        # 县
        "area": save_user["area"],
        # 经纬度
        "latitude": save_user['latitude'],
        "longitude": save_user['longitude'],
        # 打卡备注
        "description": save_user["desc"],
        "planId": save_user['planId'],
        # 签到时间标识 上午或下午
        "type": 'START',
        # 设备标识
        "device": 'Android',

        "distance": None,
        "content": None,
        "lastAddress": None,
        "lastDetailAddress": save_user["address"],
        "attendanceId": None,
        "createBy": None,
        "createTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "images": None,
        "isDeleted": None,
        "isReplace": None,
        "modifiedBy": None,
        "modifiedTime": None,
        "schoolId": None,
        "state": "NORMAL",
        "teacherId": None,
        "stuId": None,
        "attendanceType": None,
        "username": None,
        "attachments": None,
        "userId": save_user["userId"],
        "isSYN": None,
        "studentId": None,
        "applyState": None,
        "studentNumber": None,
        "headImg": None,
        "attendenceTime": None,
        "depName": None,
        "majorName": None,
        "className": None,
        "logDtoList": None,
        "t": AES.Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000))),
    }
    try:
        res = requests.post(url="https://api.moguding.net:9000/attendence/clock/v2/save", headers=headers,
                            data=json.dumps(data), ).json()

        print("    请求成功\n", end="")
    except:
        print("    请求失败")
        return {
            "sign": "请求失败",
            "position": "签到",
            "characteristic_push": push.push(push_user=save_user, createTime="请手动签到")
        }
    if res['code'] == 200:
        # try:
        #     confirm_check_text = GetConfirmCheck(confirm_check_user=save_user, Ua=Ua)
        #     if res['data']['attendanceId'] == confirm_check_text['attendanceId']:
        #         Writ(writ_user=save_user, save_time=res["data"]["createTime"])
        #         return {
        #             "sign": res['code'],
        #             "position": "签到",
        #             "characteristic_push": push.push(push_user=save_user, createTime=res["data"]["createTime"], savecode=res['code'])
        #         }
        #     elif '请求失败' in confirm_check_text['sign']:
        return {
            "sign": res['code'],
            "position": "签到",
            "characteristic_push": push.push(push_user=save_user, createTime=res["data"]["createTime"],
                                             savecode=res['code'])
        }
        #     else:
        #         return {
        #             "sign": res['msg'],
        #             "position": "签到 ——》 记录",
        #             "characteristic_push": push.push(push_user=save_user, createTime="请手动签到")
        #         }
        # except:
        #     return {
        #         "sign": res['msg'],
        #         "position": "签到->记录->签到日志",
        #         "characteristic_push": push.push(push_user=save_user, createTime="请手动签到")
        #     }

    else:
        print(f"\n    错误原因  {res['msg']}")
        return {
            "sign": res['msg'],
            "position": "签到",
            "characteristic_push": push.push(push_user=save_user, createTime="请手动签到")
        }
